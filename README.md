# Laboratorio S12 · Rompe la arquitectura (`lab-fallas`)

> **AIS86 Arquitectura de Software · UNAMBA**  
> Contenedores, balanceo de carga, estado compartido, orquestación con Kubernetes y despliegue administrado en AWS.

Este repositorio contiene el código, las configuraciones, la automatización para **GitHub Actions / Codespaces** y la documentación completa con evidencia real de las dos guías del Laboratorio S12:

- 📄 [GUIA_LAB_S12.html](./GUIA_LAB_S12.html) — Sesión 1: Experimentos locales (Docker, Docker Compose + `nginx` + Redis, Kubernetes con `kind`).
- 📄 [GUIA_LAB_S12_AWS.html](./GUIA_LAB_S12_AWS.html) — Sesión 2: Despliegue de la misma imagen en AWS (ECR + ECS Fargate + ALB).
- 📊 **[docs/fallas-s12.md](./docs/fallas-s12.md)** — **Entregable principal** con la tabla de experimentos (`A2–A3`, `B2`, `B3`, `B4`, `C3–C4`, `C6`, `C7`), resultados reales ejecutados y análisis arquitectónico.
- ☁️ **[docs/guia-aws-s12.md](./docs/guia-aws-s12.md)** — Documentación paso a paso de la arquitectura AWS, equivalencias, Puntos de Control y limpieza de recursos.

---

## 1. Las 4 piezas de arquitectura que demuestra el proyecto

| Pieza | Qué resuelve | Implementación Local | Implementación AWS |
|---|---|---|---|
| **Contenedor** | Empaqueta código y dependencias de forma reproducible | Docker (`app/Dockerfile`) | Amazon ECR + Fargate |
| **Balanceador** | Reparte tráfico entre réplicas y oculta caídas/latencias | `nginx` (Capa 7) / `Service` K8s (Capa 4) | AWS ALB + Target Group (Capa 7) |
| **Orquestador** | Mantiene el estado deseado (`replicas`), revive pods y controla despliegues | Kubernetes (`k8s/app.yaml`) | Amazon ECS Service + Circuit Breaker |
| **Clúster** | Agrupa múltiples nodos para tolerar la pérdida de una máquina completa | `kind` 3 nodos (`k8s/kind-cluster.yaml`) | AWS Fargate (*serverless* multi-AZ) |

---

## 2. Estructura del repositorio y explicación del código

```text
lab-fallas/
├── app/
│   ├── main.py                  # API FastAPI con endpoints de falla controlada
│   ├── Dockerfile               # Imagen Python 3.12-slim no-root (usuario appuser)
│   ├── requirements.txt         # fastapi, uvicorn, redis
│   └── .dockerignore
├── nginx/
│   ├── nginx.conf               # Balanceador Capa 7 bien configurado (+ least_conn opcional)
│   └── nginx-defectuoso.conf    # Balanceador defectuoso (max_fails=0, proxy_next_upstream off)
├── monitor/
│   └── index.html               # Panel visual en tiempo real (400 cuadros por réplica/error)
├── k8s/
│   ├── kind-cluster.yaml        # Clúster local de 3 nodos (1 control-plane + 2 workers)
│   └── app.yaml                 # Deployment (3 réplicas + probes + tolerations) y Service NodePort
├── compose.yaml                 # Orquestación local: 3 réplicas API + nginx + Redis + perfil monitor
├── docs/
│   ├── fallas-s12.md            # Entregable oficial con evidencias reales de cada experimento
│   └── guia-aws-s12.md          # Guía y equivalencias de la sesión AWS (ECR + ECS + ALB)
├── .github/workflows/
│   └── lab-s12.yml              # CI en GitHub Actions que ejecuta Partes A, B y C automáticamente
└── .devcontainer/
    └── devcontainer.json        # Entorno listo para GitHub Codespaces (Docker + kubectl + kind)
```

### Detalle técnico de cada componente

#### 1) Servicio API (`app/main.py` y `app/Dockerfile`)
Servicio FastAPI servido por `uvicorn` en el puerto `8000`:

| Endpoint | Método | Comportamiento |
|---|---|---|
| `/` | `GET` | Devuelve JSON con `replica` (`socket.gethostname()`), `contador`, `contador_en`, `version` y `lento`. Si existe `REDIS_URL`, incrementa la clave compartida `visitas` en Redis; si no, usa un entero en memoria local (`contador_local`). |
| `/health` | `GET` | Devuelve `200 {"ok": true}`. Si la variable de entorno `ROMPER_HEALTH=1`, responde `500 {"ok": false}` para probar *health checks* y *rollbacks*. |
| `/crash` | `POST` | Ejecuta `os._exit(1)`, matando el proceso de inmediato sin responder (simula un fallo fatal o *OOM Kill*). |
| `/lento` | `POST` | Activa o desactiva un retardo artificial (`time.sleep(2)`) únicamente en la réplica que recibió la petición. |

> **¿Por qué envía `Connection: close`?**  
> La función `cerrar(resp)` cierra la conexión HTTP al final de cada respuesta para que el `Service` de Kubernetes (balanceador de **Capa 4** que decide por conexión TCP) reparta cada petición entre pods distintos en el monitor visual.

El `Dockerfile` aplica buenas prácticas: imagen base ligera (`python:3.12-slim`), copia primero `requirements.txt` para aprovechar caché de capas, crea un usuario sin privilegios (`appuser`) y expone el puerto `8000`.

#### 2) Balanceador `nginx` (`nginx/nginx.conf` vs `nginx/nginx-defectuoso.conf`)
- **Configuración buena (`nginx.conf`):**
  - `server api:8000 max_fails=1 fail_timeout=10s;` — *health check* pasivo: tras 1 fallo retira la réplica caída durante 10 s.
  - `proxy_next_upstream error timeout;` — si una réplica no responde, reintenta la **misma petición** en otra réplica sana antes de contestar al cliente (0 errores visibles).
  - `# least_conn;` — comentado por defecto (*round robin*); al descomentarlo evita saturar réplicas lentas.
- **Configuración defectuosa (`nginx-defectuoso.conf`):**
  - `max_fails=0` (nunca marca la réplica como caída) y `proxy_next_upstream off` (no reintenta). El cliente recibe errores `502`/`504` en ~1 de cada 3 peticiones.

#### 3) Monitor visual (`monitor/index.html`)
Aplicación HTML/JS sin dependencias que:
- En `:8080` apunta por defecto a `/api/` (Parte B con `nginx`); en `:8090` apunta a `http://localhost:30080/` (Parte C con Kubernetes) o a la URL de un ALB de AWS.
- Ejecuta 1, 4 u 8 bucles concurrentes de `fetch`, colorea 400 cuadritos según la réplica que respondió (rojo = error HTTP/red) y expone botones para disparar `POST /crash` y `POST /lento`.

#### 4) Manifiestos de Kubernetes (`k8s/kind-cluster.yaml` y `k8s/app.yaml`)
- `kind-cluster.yaml`: crea 3 nodos en Docker (`ais86-control-plane`, `ais86-worker`, `ais86-worker2`) y mapea `localhost:30080` al `NodePort` del clúster.
- `app.yaml`:
  - `Deployment` con `replicas: 3` (estado deseado).
  - `readinessProbe` (`GET /health` cada 2 s) para sacar pods no listos del `Service`.
  - `livenessProbe` (`GET /health` cada 5 s) para reiniciar contenedores bloqueados o rotos.
  - `tolerations` de `15s` en `node.kubernetes.io/unreachable` y `not-ready` (en lugar de los 5 min por defecto) para acelerar la demostración de caída de nodo en el Exp. C6.
  - `Service` tipo `NodePort` (`30080`) con selector `app: api` (descubrimiento de servicios dinámico por etiquetas, sin IPs fijas).

---

## 3. Cómo ejecutar el laboratorio

### Opción A · Ejecución local (Windows PowerShell / Linux / macOS)

```powershell
# Parte A: Contenedor único
docker build -t lab-fallas:1.0 ./app
docker run -d -p 8000:8000 --name solo lab-fallas:1.0
curl.exe http://localhost:8000/
curl.exe -X POST http://localhost:8000/crash
docker rm -f solo

# Parte B: 3 réplicas + nginx + Redis
docker compose up -d
# Abrir monitor en http://localhost:8080
# Activar Redis (Exp. B3):
$env:REDIS_URL="redis://redis:6379/0"; docker compose up -d api; docker compose restart lb
docker compose down

# Parte C: Clúster Kubernetes de 3 nodos con kind
kind create cluster --config k8s/kind-cluster.yaml
kind load docker-image lab-fallas:1.0 --name ais86
kubectl apply -f k8s/app.yaml
docker compose --profile monitor up -d monitor
# Abrir monitor en http://localhost:8090 (apuntando a http://localhost:30080/)
# Limpieza al terminar:
kind delete cluster --name ais86
docker compose --profile monitor down
```

### Opción B · Ejecutar directamente en GitHub

1. **GitHub Actions (automático y sin instalar nada):**
   - Al subir este repositorio a GitHub, el workflow [`.github/workflows/lab-s12.yml`](./.github/workflows/lab-s12.yml) se ejecuta en *runners* Ubuntu y corre automáticamente:
     - **Job `parte-a-y-b-docker`**: construye la imagen, prueba A1–A3, B1, B2 bueno vs. defectuoso y B3 con Redis.
     - **Job `parte-c-kubernetes`**: levanta el clúster `kind` de 3 nodos, despliega `k8s/app.yaml`, ejecuta C3, C4, C5, C7 (`ROMPER_HEALTH=1` + `rollback`) y limpia el clúster.
   - También puede lanzarse manualmente desde la pestaña **Actions → Lab S12 - Rompe la arquitectura → Run workflow**.

2. **GitHub Codespaces (interactivo con monitor visual en el navegador):**
   - Abre el repositorio en GitHub → botón **Code → Codespaces → Create codespace on main**.
   - El archivo [`.devcontainer/devcontainer.json`](./.devcontainer/devcontainer.json) configura Docker-in-Docker, `kubectl`, `kind` y reenvía los puertos `8000`, `8080`, `8090` y `30080` automáticamente.
