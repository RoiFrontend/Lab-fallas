import os
import base64
import subprocess

def to_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    return ""

img_alg = to_base64("c:/Users/roger/Downloads/lab-fallas/lab-fallas/docs/graficos/comparativa_algoritmos.png")
img_little = to_base64("c:/Users/roger/Downloads/lab-fallas/lab-fallas/docs/graficos/ley_de_little_escalabilidad.png")
img_hc = to_base64("c:/Users/roger/Downloads/lab-fallas/lab-fallas/docs/evidencias/aws_target_group_health_check.png")
img_mon = to_base64("c:/Users/roger/Downloads/lab-fallas/lab-fallas/docs/evidencias/monitor_errores_red.png")

img_b1 = to_base64("c:/Users/roger/Downloads/lab-fallas/lab-fallas/docs/evidencias/monitor_B1_round_robin.png")
img_b2a = to_base64("c:/Users/roger/Downloads/lab-fallas/lab-fallas/docs/evidencias/monitor_B2a_failover_exitoso.png")
img_b2b = to_base64("c:/Users/roger/Downloads/lab-fallas/lab-fallas/docs/evidencias/monitor_B2b_nginx_defectuoso_rojos.png")
img_b3 = to_base64("c:/Users/roger/Downloads/lab-fallas/lab-fallas/docs/evidencias/monitor_B3_redis_compartido.png")
img_b4a = to_base64("c:/Users/roger/Downloads/lab-fallas/lab-fallas/docs/evidencias/monitor_B4a_lenta_round_robin.png")
img_b4b = to_base64("c:/Users/roger/Downloads/lab-fallas/lab-fallas/docs/evidencias/monitor_B4b_lenta_least_conn.png")

img_c3 = to_base64("c:/Users/roger/Downloads/lab-fallas/lab-fallas/docs/evidencias/monitor_C3_k8s_3replicas.png")
img_c5 = to_base64("c:/Users/roger/Downloads/lab-fallas/lab-fallas/docs/evidencias/monitor_C5_k8s_5replicas.png")
img_c6 = to_base64("c:/Users/roger/Downloads/lab-fallas/lab-fallas/docs/evidencias/monitor_C6_k8s_nodo_caido.png")
img_c7 = to_base64("c:/Users/roger/Downloads/lab-fallas/lab-fallas/docs/evidencias/monitor_C7_k8s_despliegue_roto.png")

html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Informe Lab S12 · Rompe la arquitectura · AIS86 UNAMBA</title>
<style>
  @page {{
    size: A4;
    margin: 20mm 18mm;
    @bottom-center {{
      content: "Página " counter(page);
    }}
  }}
  body {{
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    font-size: 10.5pt;
    line-height: 1.5;
    color: #1b1e2b;
    margin: 0 auto;
    max-width: 820px;
    padding: 24px;
    background: #fff;
  }}
  h1 {{
    color: #1d3b8f;
    font-size: 20pt;
    margin: 8px 0 4px;
    text-align: center;
  }}
  h2 {{
    color: #1d3b8f;
    font-size: 13.5pt;
    border-bottom: 2px solid #1d3b8f;
    padding-bottom: 4px;
    margin-top: 24px;
    page-break-after: avoid;
  }}
  h3 {{
    color: #2b4c9c;
    font-size: 11pt;
    margin-top: 14px;
    page-break-after: avoid;
  }}
  .portada {{
    text-align: center;
    border-bottom: 3px double #1d3b8f;
    padding-bottom: 20px;
    margin-bottom: 25px;
  }}
  .univ {{
    font-size: 12pt;
    font-weight: bold;
    color: #1d3b8f;
    margin-bottom: 4px;
  }}
  .fac {{
    font-size: 10pt;
    color: #555;
    margin-bottom: 14px;
  }}
  .subtit {{
    font-size: 11pt;
    color: #555;
    font-style: italic;
    margin-top: 6px;
  }}
  .meta-box {{
    background: #f1f3f8;
    border: 1px solid #c9cfdd;
    border-radius: 6px;
    padding: 10px 16px;
    margin: 18px 0;
    font-size: 9.5pt;
  }}
  .meta-box table {{
    width: 100%;
    border-collapse: collapse;
    margin: 0;
  }}
  .meta-box td {{
    padding: 3px 6px;
    border: none;
    background: transparent;
  }}
  .meta-box td.label {{
    font-weight: bold;
    color: #1d3b8f;
    width: 28%;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 9pt;
    page-break-inside: avoid;
  }}
  th, td {{
    border: 1px solid #c9cfdd;
    padding: 6px 8px;
    text-align: left;
    vertical-align: top;
  }}
  th {{
    background: #1d3b8f;
    color: #fff;
    font-weight: 600;
  }}
  tr:nth-child(even) td {{
    background: #f8fafd;
  }}
  .img-box {{
    text-align: center;
    margin: 14px 0;
    page-break-inside: avoid;
  }}
  .img-box img {{
    max-width: 95%;
    height: auto;
    border: 1px solid #d6dbe8;
    border-radius: 6px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
  }}
  .img-cap {{
    font-size: 8.5pt;
    color: #555;
    font-style: italic;
    margin-top: 4px;
  }}
  .box {{
    border-left: 4px solid #139a5e;
    background: #eefaf3;
    padding: 8px 12px;
    border-radius: 0 6px 6px 0;
    margin: 12px 0;
    font-size: 9.5pt;
  }}
  .box-blue {{
    border-left: 4px solid #1d3b8f;
    background: #eef2fc;
    padding: 8px 12px;
    border-radius: 0 6px 6px 0;
    margin: 12px 0;
    font-size: 9.5pt;
  }}
  .page-break {{
    page-break-before: always;
  }}
  code {{
    font-family: Consolas, monospace;
    font-size: 9pt;
    background: #f1f3f8;
    padding: 1px 4px;
    border-radius: 3px;
    color: #b31d28;
  }}
</style>
</head>
<body>

<div class="portada">
  <div class="univ">UNIVERSIDAD NACIONAL MICAELA BASTIDAS DE APURÍMAC</div>
  <div class="fac">FACULTAD DE INGENIERÍA · ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS E INFORMÁTICA</div>
  <h1>INFORME DE LABORATORIO S12<br>ROMPE LA ARQUITECTURA</h1>
  <div class="subtit">Resiliencia, Balanceo de Carga L4/L7, Persistencia Distribuida y Orquestación (Local y AWS ECS Fargate + ALB)</div>
</div>

<div class="meta-box">
  <table>
    <tr><td class="label">ASIGNATURA:</td><td>AIS86 - Arquitectura de Software</td></tr>
    <tr><td class="label">ESTUDIANTE / EQUIPO:</td><td>Roger Paniura Ramos (RoiFrontend)</td></tr>
    <tr><td class="label">DOCENTE:</td><td>Docente de Arquitectura de Software · UNAMBA</td></tr>
    <tr><td class="label">REPOSITORIO GITHUB:</td><td><a href="https://github.com/RoiFrontend/Lab-fallas">https://github.com/RoiFrontend/Lab-fallas</a></td></tr>
    <tr><td class="label">FECHA DE EJECUCIÓN:</td><td>Noviembre 2026</td></tr>
  </table>
</div>

<h2>1. RESUMEN EJECUTIVO Y OBJETIVOS</h2>
<p>
El presente informe documenta el desarrollo integral y las pruebas experimentales del <strong>Laboratorio S12 ("Rompe la arquitectura")</strong>. 
El propósito central fue someter a prueba empírica una arquitectura de microservicios, simulando fallos críticos y demostrando qué componente 
técnico mitiga cada contingencia.
</p>
<p>
El estudio abarcó dos entornos de trabajo complementarios:
<ol>
  <li><strong>Entorno Local (Lunes):</strong> Diagnóstico de puntos únicos de falla (SPOF) en contenedores Docker, balanceo de carga en Capa 7 con NGINX, persistencia de estado desacoplada en Redis y resiliencia mediante un clúster Kubernetes multinodo (Kind).</li>
  <li><strong>Entorno en la Nube AWS (Miércoles):</strong> Migración de la misma imagen de contenedor (<code>lab-fallas:1.0</code>) hacia servicios administrados en AWS (us-east-2, Ohio): Amazon ECR (registro), AWS Fargate (cómputo serverless), Amazon ECS (orquestador con Circuit Breaker) y Application Load Balancer (ALB).</li>
</ol>
</p>

<h2>2. LAS 4 PIEZAS CLAVE DE LA ARQUITECTURA</h2>
<table>
  <tr>
    <th style="width:18%;">Pieza Clave</th>
    <th style="width:36%;">Función Arquitectónica</th>
    <th style="width:23%;">Implementación Local</th>
    <th style="width:23%;">Implementación en AWS</th>
  </tr>
  <tr>
    <td><strong>Contenedor</strong></td>
    <td>Aísla código y dependencias. Elimina el problema de "en mi máquina funciona".</td>
    <td>Docker Engine (<code>app/Dockerfile</code>)</td>
    <td>Amazon ECR + AWS Fargate</td>
  </tr>
  <tr>
    <td><strong>Balanceador</strong></td>
    <td>Distribuye peticiones entre réplicas. Detecta caídas y aísla lentitudes.</td>
    <td>NGINX 1.30 (Capa 7)</td>
    <td>Application Load Balancer (ALB)</td>
  </tr>
  <tr>
    <td><strong>Orquestador</strong></td>
    <td>Mantiene el estado deseado (<code>replicas</code>), revive tareas y ejecuta rollbacks.</td>
    <td>Kubernetes Deployment</td>
    <td>Amazon ECS + Circuit Breaker</td>
  </tr>
  <tr>
    <td><strong>Clúster</strong></td>
    <td>Agrupa máquinas físicas/virtuales para tolerar la pérdida de servidores enteros.</td>
    <td>Kind (3 nodos: control + 2 workers)</td>
    <td>Infraestructura AWS Multi-AZ</td>
  </tr>
</table>

<div class="page-break"></div>

<h2>3. DESARROLLO EXPERIMENTAL: GUÍA 1 (LOCAL)</h2>

<h3>3.1 Parte A · Contenedor Único y Análisis de Estado (A1 – A3)</h3>
<p>
Se construyó la imagen <code>lab-fallas:1.0</code>. Al correr un contenedor único expuesto en el puerto 8000:
<ul>
  <li><strong>A1:</strong> Cada petición <code>GET /</code> incrementó el contador en memoria (<code>1 -> 2 -> 3</code>).</li>
  <li><strong>A2 (Punto Único de Falla):</strong> Al invocar <code>POST /crash</code> (<code>os._exit(1)</code>), el contenedor murió de inmediato quedando en estado <code>Exited (1)</code>. El servicio quedó totalmente inoperativo ante el cliente.</li>
  <li><strong>A3 (Política de Reinicio):</strong> Con <code>--restart unless-stopped</code>, Docker revivió el contenedor en 2 segundos; sin embargo, al consultar <code>GET /</code>, <strong>el contador se reinició en 1</strong>. Conclusión: <em>"Todo lo que vive en memoria RAM del contenedor muere con él. Reiniciar no preserva el estado."</em></li>
</ul>
</p>

<h3>3.2 Parte B · Réplicas, NGINX y Persistencia con Redis (B1 – B4)</h3>
<p>
Con Docker Compose se desplegaron 3 réplicas de la API, un balanceador NGINX y Redis:
<ul>
  <li><strong>B1 (Round Robin):</strong> NGINX alternó 3 colores en el monitor de forma equitativa.</li>
  <li><strong>B2 (Balanceador Bueno vs Defectuoso):</strong> Al matar una réplica (<code>docker kill lab-fallas-api-2</code>):
    <ul>
      <li>Con <code>nginx.conf</code> (bueno): <strong>0% de errores</strong>. Sus directivas <code>max_fails=1</code> y <code>proxy_next_upstream error timeout</code> reintentaron de inmediato en otra réplica sana.</li>
      <li>Con <code>nginx-defectuoso.conf</code>: <strong>33.3% de errores HTTP 504</strong>. Al tener <code>proxy_next_upstream off</code> y <code>max_fails=0</code>, el error llegó directo al usuario.</li>
    </ul>
  </li>
  <li><strong>B3 (Estado Compartido en Redis):</strong> Al inyectar <code>REDIS_URL</code>, el estado salió del contenedor hacia Redis. Las 3 réplicas compartieron una secuencia continua (<code>1, 2, 3... 9</code>), permitiendo una arquitectura verdaderamente <em>stateless</em>.</li>
  <li><strong>B4 (Réplica Lenta: Round Robin vs Least Connections):</strong> Se inyectó retardo de 2 segundos mediante <code>POST /lento</code>. Con Round Robin, la réplica lenta siguió recibiendo el 33.3% de las peticiones. Al activar <code>least_conn;</code> en NGINX, su tráfico cayó a solo <strong>4.2%</strong>, enviando el <strong>95.8%</strong> a las réplicas rápidas.</li>
</ul>
</p>

<div class="img-box">
  <img src="{img_b1}" alt="Monitor B1 Round Robin">
  <div class="img-cap">Figura 1: Monitor visual en Experimento B1: Round Robin con 3 réplicas alternándose equitativamente (0 errores).</div>
</div>

<div class="img-box">
  <img src="{img_b2a}" alt="Monitor B2a Failover Exitoso">
  <div class="img-cap">Figura 2: Monitor visual en Experimento B2(a): Failover exitoso con NGINX bueno tras 'docker kill lab-fallas-api-2' (0 errores).</div>
</div>

<div class="img-box">
  <img src="{img_b2b}" alt="Monitor B2b NGINX Defectuoso">
  <div class="img-cap">Figura 3: Monitor visual en Experimento B2(b): Configuración defectuosa sin reintentos; se observan 34 cuadros rojos (33.7% error 504).</div>
</div>

<div class="img-box">
  <img src="{img_b3}" alt="Monitor B3 Redis Compartido">
  <div class="img-cap">Figura 4: Monitor visual en Experimento B3: Persistencia centralizada con Redis; secuencia de contador global e incremental continua.</div>
</div>

<div class="img-box">
  <img src="{img_b4a}" alt="Monitor B4a Lenta Round Robin">
  <div class="img-cap">Figura 5: Monitor visual en Experimento B4(a): Réplica lenta bajo Round Robin (recibe ~35% del tráfico a 2063 ms).</div>
</div>

<div class="img-box">
  <img src="{img_b4b}" alt="Monitor B4b Lenta Least Connections">
  <div class="img-cap">Figura 6: Monitor visual en Experimento B4(b): Réplica lenta bajo Least Connections (tráfico redirigido al 98% a réplicas sanas).</div>
</div>

<div class="img-box">
  <img src="{img_alg}" alt="Comparativa de Algoritmos">
  <div class="img-cap">Figura 7: Tráfico atendido en Experimento B4: Round Robin (ciego) vs. Least Connections (adaptativo).</div>
</div>

<h3>3.3 Parte C · Clúster y Orquestación con Kubernetes Kind (C1 – C8)</h3>
<p>
Se levantó un clúster Kubernetes de 3 nodos (<code>ais86-control-plane</code>, <code>ais86-worker</code>, <code>ais86-worker2</code>):
<ul>
  <li><strong>C3 (Autocuración de Pods):</strong> Al borrar un pod, el Deployment creó de inmediato un sustituto en 4 segundos, conservando el estado deseado (<code>replicas: 3</code>).</li>
  <li><strong>C4 (Crash de Proceso):</strong> Al invocar <code>POST /crash</code>, kubelet reinició el contenedor (<code>RESTARTS: 1</code>).</li>
  <li><strong>C5 (Escalado Dinámico):</strong> Al escalar a 5 réplicas (<code>kubectl scale</code>), el <code>Service</code> descubrió los 2 nuevos pods sin reiniciar el balanceador, desplegando 5 colores distintos en el monitor.</li>
  <li><strong>C6 (Caída de Nodo Físico):</strong> Al detener el nodo <code>ais86-worker</code>, Kubernetes esperó 15 segundos (toleration), marcó el nodo como <code>NotReady</code> y reprogramó los pods en <code>ais86-worker2</code>.</li>
  <li><strong>C7 (Despliegue Roto y Rollback):</strong> Con <code>ROMPER_HEALTH=1</code>, el pod nuevo nunca pasó el <code>readinessProbe</code> (0/1). Kubernetes mantuvo intactos los 3 pods sanos, garantizando 0 errores en el monitor hasta ejecutar <code>kubectl rollout undo</code>.</li>
</ul>
</p>

<div class="img-box">
  <img src="{img_c3}" alt="Monitor C3 K8s 3 Replicas">
  <div class="img-cap">Figura 8: Monitor visual en Experimento C3: 3 Pods en Kubernetes Kind atendiendo en NodePort 30080 (0 errores).</div>
</div>

<div class="img-box">
  <img src="{img_c5}" alt="Monitor C5 K8s 5 Replicas">
  <div class="img-cap">Figura 9: Monitor visual en Experimento C5: Escalamiento dinámico a 5 Pods con 5 colores distintos descubiertos por el Service (0 errores).</div>
</div>

<div class="img-box">
  <img src="{img_c6}" alt="Monitor C6 K8s Nodo Caido">
  <div class="img-cap">Figura 10: Monitor visual en Experimento C6: Cuadros rojos en la ventana de detección al apagar el nodo worker (tolerancia de 15s) antes de la reprogramación.</div>
</div>

<div class="img-box">
  <img src="{img_c7}" alt="Monitor C7 K8s Despliegue Roto">
  <div class="img-cap">Figura 11: Monitor visual en Experimento C7: Protección de despliegue progresivo (readinessProbe); los 3 pods sanos atienden con 0 errores.</div>
</div>

<div class="page-break"></div>

<h2>4. DESARROLLO EXPERIMENTAL: GUÍA 2 (AWS CLOUD)</h2>
<p>
Se implementó la arquitectura en Amazon Web Services (Región Ohio <code>us-east-2</code>):
<ul>
  <li><strong>Amazon ECR:</strong> Repositorio privado <code>280161530063.dkr.ecr.us-east-2.amazonaws.com/lab-fallas:1.0</code>.</li>
  <li><strong>AWS Fargate:</strong> Cómputo serverless con 0.25 vCPU y 0.5 GB de memoria por tarea.</li>
  <li><strong>Amazon ECS:</strong> Orquestación del servicio <code>api</code> (2 tareas deseadas).</li>
  <li><strong>Application Load Balancer (ALB):</strong> DNS <code>lab-fallas-alb-154417865.us-east-2.elb.amazonaws.com</code>.</li>
</ul>
</p>

<h3>4.1 Demostración de los 3 Puntos de Control Exigidos</h3>
<div class="box">
  <strong>✅ PUNTO DE CONTROL 1: Balanceo y Salud en la Nube</strong><br>
  El Application Load Balancer enrutó tráfico equitativamente entre las 2 tareas Fargate registradas en el Target Group <code>lab-fallas-tg</code>. Ambas instancias respondieron con estado <code>healthy</code> al chequeo sobre <code>/health</code>. En el monitor visual (puerto 8090) se observó la alternancia continua de 2 colores sin errores.
</div>

<div class="img-box">
  <img src="{img_hc}" alt="Configuración de Health Checks en AWS">
  <div class="img-cap">Figura 12: Parámetros optimizados de Comprobación de Estado en AWS Target Group (Ruta /health, intervalo 10s, umbral 2).</div>
</div>

<div class="box">
  <strong>✅ PUNTO DE CONTROL 2: Sustitución Automática y Algoritmo Least Outstanding Requests</strong><br>
  <strong>1. Caída de Tarea:</strong> Al disparar <code>POST /crash</code>, la tarea afectada murió. Amazon ECS registró en sus eventos la desvinculación inmediata y lanzó en menos de 40 segundos una tarea de reemplazo (<code>started 1 tasks</code>) para restituir el estado deseado.<br>
  <strong>2. Cambio de Algoritmo:</strong> Se volvió lenta una réplica (2000 ms). Con Round Robin recibía ~50% de peticiones. Al editar los atributos del Target Group y configurar <em>Least outstanding requests</em>, el ALB redujo drásticamente el tráfico hacia la réplica degradada, priorizando la réplica rápida.
</div>

<div class="box">
  <strong>✅ PUNTO DE CONTROL 3: Despliegue Roto y Rollback Automático</strong><br>
  Se generó una revisión de la tarea con <code>ROMPER_HEALTH=1</code>. Las tareas nuevas fallaron <code>/health</code> (HTTP 500) y fueron marcadas <code>unhealthy</code>. Al acumular 3 fallos consecutivos, el <strong>Deployment Circuit Breaker</strong> abortó la actualización e inició un <strong>Rollback automático</strong> hacia la revisión funcional. En todo momento el monitor visual no mostró cuadros rojos, demostrando que el cliente jamás fue expuesto a la versión rota.
</div>

<div class="img-box">
  <img src="{img_mon}" alt="Monitor Visual de Errores y Diagnóstico">
  <div class="img-cap">Figura 13: Diagnóstico en Monitor Visual: Registro en tiempo real de peticiones HTTP y cuadros de control de tráfico.</div>
</div>

<h3>4.2 Análisis de Capacidad y Ley de Little (Prueba C4)</h3>
<p>
Mediante el script <code>capacidad.py</code> se modeló el comportamiento del servicio bajo concurrencia. Según la <strong>Ley de Little</strong>:
<center><code>L = λ × W &nbsp;→&nbsp; Clientes en vuelo = req/s × latencia promedio</code></center>
Al elevar los clientes simultáneos de 5 a 20 en una tarea Fargate con 0.25 vCPU, la CPU se saturó cerca del 100%, manteniendo la tasa plana (~325 req/s) mientras la latencia p50 creció de 3 ms a 35 ms y p95 a 72 ms. Al escalar a 4 tareas, la latencia retornó a 3 ms.
</p>

<div class="img-box">
  <img src="{img_little}" alt="Ley de Little y Capacidad">
  <div class="img-cap">Figura 14: Curva empírica de latencia según Ley de Little en Fargate (1 Tarea saturada vs. 4 Tareas escaladas).</div>
</div>

<div class="page-break"></div>

<h2>5. MATRIZ OFICIAL DE RESULTADOS Y EVIDENCIAS REALES</h2>
<table>
  <tr>
    <th style="width:10%;">Exp.</th>
    <th style="width:25%;">Qué rompimos</th>
    <th style="width:35%;">Qué vimos (Evidencia Real)</th>
    <th style="width:30%;">Qué pieza lo resolvió y cómo</th>
  </tr>
  <tr>
    <td><strong>A2–A3</strong></td>
    <td>Contenedor único detenido con <code>POST /crash</code>.</td>
    <td>A2: curl devolvió Empty reply y estado Exited (1).<br>A3: Con <code>--restart unless-stopped</code> revivió en 2s, pero el contador se reinició en 1.</td>
    <td><strong>Política de reinicio de Docker Engine</strong> revivió el contenedor, demostrando que reiniciar no preserva memoria local.</td>
  </tr>
  <tr>
    <td><strong>B2</strong></td>
    <td>Réplica detenida con NGINX bueno vs defectuoso.</td>
    <td>NGINX bueno: 12 peticiones OK (HTTP 200), 0 errores.<br>NGINX defectuoso: 4 fallas (HTTP 502/504), 33% de error visible.</td>
    <td><strong>Balanceador NGINX Capa 7</strong> con <code>max_fails=1</code> y <code>proxy_next_upstream error timeout</code> reintentó en réplica sana.</td>
  </tr>
  <tr>
    <td><strong>B3</strong></td>
    <td>Estado en RAM inconsistente vs Redis.</td>
    <td>En RAM: contadores aislados 1,1,1, 2,2,2.<br>Con Redis: secuencia continua 1 -> 9 compartida por las 3 réplicas.</td>
    <td><strong>Motor de estado compartido (Redis)</strong>. La arquitectura se desacopló haciéndose stateless.</td>
  </tr>
  <tr>
    <td><strong>B4</strong></td>
    <td>Réplica degradada con latencia de 2s.</td>
    <td>Round Robin: la réplica lenta recibió 8/24 (33.3%) a 2004 ms.<br>least_conn: bajó a 1/24 (4.2%) y las rápidas atendieron 95.8%.</td>
    <td><strong>Algoritmo adaptativo (least_conn)</strong>. Enruta hacia la réplica con menor cantidad de conexiones activas.</td>
  </tr>
  <tr>
    <td><strong>C3–C4</strong></td>
    <td>Pod borrado y proceso crasheado en Kubernetes.</td>
    <td>C3: Reemplazo creado en 4s con nueva IP.<br>C4: kubelet reinició contenedor (RESTARTS: 1). Tráfico sin interrupción.</td>
    <td><strong>Orquestador Kubernetes</strong> (Deployment controller y kubelet) reconcilió el estado deseado <code>replicas: 3</code>.</td>
  </tr>
  <tr>
    <td><strong>C6</strong></td>
    <td>Apagado total de un nodo worker físico.</td>
    <td>A los 15s errores breves. A los 30s nodo NotReady. A los 45s los 5 pods operaban en worker2.</td>
    <td><strong>Clúster multinodo + Tolerations (15s)</strong>. Reprogramó la carga en el nodo sano disponible.</td>
  </tr>
  <tr>
    <td><strong>C7</strong></td>
    <td>Despliegue de versión rota (ROMPER_HEALTH=1).</td>
    <td>Pod nuevo bloqueado en 0/1 Running con RESTARTS: 2. Los 3 pods sanos mantuvieron 12 OK y 0 errores.</td>
    <td><strong>ReadinessProbe + Rolling Update de Kubernetes</strong>. Impide retirar réplicas sanas si la nueva no pasa su health check.</td>
  </tr>
</table>

<h2>6. CONCLUSIONES Y RESPUESTAS ANTE EL DOCENTE</h2>

<h3>6.1 Pregunta Final de la Guía</h3>
<div class="box-blue">
  <strong>«En su sistema, ¿cuál de las fallas de hoy les dolería más y qué pieza de las cuatro la previene?»</strong><br><br>
  <strong>Respuesta del equipo:</strong><br>
  La falla más destructiva en producción es el <strong>despliegue inadvertido de una versión rota</strong> o la <strong>corrupción de datos por pérdida de estado en memoria</strong>. La caída total del servicio se previene mediante la articulación del <strong>Orquestador (Kubernetes / AWS ECS)</strong> con health checks rigurosos (<code>readinessProbe</code> / Target Group checks) y <strong>Circuit Breakers con rollback automático</strong>, evitando que una versión dañada reciba tráfico de clientes. A su vez, el <strong>Balanceador Capa 7 (NGINX / AWS ALB)</strong> aísla anomalías y reintenta peticiones en vuelo, mientras que el almacenamiento distribuido en <strong>Redis</strong> garantiza que la muerte o rotación de cualquier réplica sea transparente para el usuario final.
</div>

<h3>6.2 Protocolo de Limpieza en AWS</h3>
<p>
Para garantizar cero costos posteriores de facturación, se ejecutó la destrucción controlada de los recursos en AWS:
<ol>
  <li>Eliminación del servicio ECS <code>api</code> (Force delete).</li>
  <li>Eliminación del Application Load Balancer <code>lab-fallas-alb</code> y Target Group <code>lab-fallas-tg</code>.</li>
  <li>Eliminación del clúster ECS <code>lab-fallas</code>.</li>
  <li>Detención de contenedores locales con <code>docker compose --profile monitor down</code>.</li>
</ol>
Costo total registrado en la cuenta: <strong>US$ 0.16</strong>.
</p>

</body>
</html>
"""

html_path = "c:/Users/roger/Downloads/lab-fallas/lab-fallas/INFORME_LAB_S12_ROMPE_LA_ARQUITECTURA.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML generado en: {html_path}")

# Convertir a PDF usando Edge headless
pdf_path = "c:/Users/roger/Downloads/lab-fallas/lab-fallas/INFORME_LAB_S12_ROMPE_LA_ARQUITECTURA.pdf"
edge_exe = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
cmd = [
    edge_exe,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    f"file:///{html_path}"
]

try:
    subprocess.run(cmd, check=True)
    print(f"PDF generado exitosamente en: {pdf_path}")
except Exception as e:
    print(f"Error generando PDF: {e}")
