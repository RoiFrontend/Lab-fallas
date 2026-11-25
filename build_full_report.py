import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_report():
    doc = Document()
    
    # Configuración de márgenes (2.5 cm = 0.984 inches)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.98)
        section.bottom_margin = Inches(0.98)
        section.left_margin = Inches(0.98)
        section.right_margin = Inches(0.98)
        
    # Estilos de fuente normal
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(10.5)
    font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    style.paragraph_format.line_spacing = 1.15
    style.paragraph_format.space_after = Pt(4)

    # Colores corporativos
    NAVY = RGBColor(0x1D, 0x3B, 0x8F)
    GREEN = RGBColor(0x13, 0x9A, 0x5E)
    DARK = RGBColor(0x1B, 0x1E, 0x2B)
    GRAY = RGBColor(0x55, 0x55, 0x55)

    # ========================== PORTADA ==========================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("UNIVERSIDAD NACIONAL MICAELA BASTIDAS DE APURÍMAC\nFACULTAD DE INGENIERÍA\nESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS E INFORMÁTICA")
    r_inst.font.size = Pt(12)
    r_inst.font.bold = True
    r_inst.font.color.rgb = NAVY

    doc.add_paragraph("\n" * 2)

    p_tit = doc.add_paragraph()
    p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_tit = p_tit.add_run("INFORME DE LABORATORIO S12\nROMPE LA ARQUITECTURA\nRESILIENCIA, BALANCEO DE CARGA Y ALTA DISPONIBILIDAD (LOCAL Y AWS)")
    r_tit.font.size = Pt(18)
    r_tit.font.bold = True
    r_tit.font.color.rgb = NAVY

    doc.add_paragraph("\n")

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Contenedores, Balanceo de Carga L4/L7, Estado Distribuido, Orquestación con Kubernetes y Servicios Administrados en AWS ECS Fargate + ALB")
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = GRAY

    doc.add_paragraph("\n" * 4)

    # Cuadro de metadatos
    tbl_meta = doc.add_table(rows=5, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("ASIGNATURA:", "AIS86 - Arquitectura de Software"),
        ("ESTUDIANTE / EQUIPO:", "Roger Paniura Ramos (RoiFrontend)"),
        ("DOCENTE:", "Docente de Arquitectura de Software - UNAMBA"),
        ("REPOSITORIO GITHUB:", "https://github.com/RoiFrontend/Lab-fallas"),
        ("FECHA DE EJECUCIÓN:", "Noviembre 2026")
    ]
    for i, (k, v) in enumerate(meta_data):
        row = tbl_meta.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.5)
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(k)
        r0.font.bold = True
        r0.font.size = Pt(10)
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(v)
        r1.font.size = Pt(10)
        set_cell_background(c0, "F1F3F8")
        set_cell_background(c1, "FFFFFF")

    doc.add_page_break()

    # ========================== 1. RESUMEN EJECUTIVO ==========================
    h1 = doc.add_heading("1. RESUMEN EJECUTIVO Y OBJETIVOS", level=1)
    h1.runs[0].font.color.rgb = NAVY
    h1.runs[0].font.bold = True

    p = doc.add_paragraph(
        "El presente informe documenta el desarrollo integral y la validación empírica del Laboratorio S12 ('Rompe la arquitectura'). "
        "El objetivo fundamental no reside en la mera codificación de un microservicio, sino en observar, provocar y mitigar escenarios "
        "reales de falla sobre una arquitectura distribuida, determinando con precisión qué componente técnico neutraliza cada riesgo de disponibilidad."
    )
    p = doc.add_paragraph(
        "El laboratorio se estructuró en dos grandes fases complementarias:\n"
        "1. Fase Local (Lunes): Análisis de puntos únicos de falla (SPOF) en contenedores Docker, balanceo de carga en Capa 7 con NGINX, "
        "persistencia distribuida en memoria mediante Redis, y orquestación resiliente en clúster local de 3 nodos mediante Kubernetes (Kind).\n"
        "2. Fase Nube (Miércoles - AWS): Migración de la misma imagen de contenedor (lab-fallas:1.0) hacia infraestructura administrada en la nube de Amazon Web Services, "
        "haciendo uso de Amazon ECR (registro), AWS Fargate (cómputo serverless), Amazon ECS (orquestador de tareas con Circuit Breaker) "
        "y Application Load Balancer (ALB), demostrando los 3 Puntos de Control exigidos."
    )

    # ========================== 2. LAS 4 PIEZAS ==========================
    h1 = doc.add_heading("2. LAS CUATRO PIEZAS CLAVE DE LA ARQUITECTURA", level=1)
    h1.runs[0].font.color.rgb = NAVY
    h1.runs[0].font.bold = True

    doc.add_paragraph(
        "Para construir sistemas de alta resiliencia y tolerancia a fallos, la arquitectura desacopla cuatro funciones críticas. "
        "La siguiente tabla resume la función de cada pieza y su equivalencia exacta entre el entorno local y AWS:"
    )

    tbl_piezas = doc.add_table(rows=5, cols=4)
    tbl_piezas.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Pieza Clave", "Función en la Arquitectura", "Implementación Local", "Implementación en AWS"]
    for j, h in enumerate(headers):
        cell = tbl_piezas.rows[0].cells[j]
        set_cell_background(cell, "1D3B8F")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.size = Pt(9.5)

    filas_piezas = [
        ("Contenedor", "Empaqueta la aplicación y sus librerías aisladas. Garantiza portabilidad y reproducibilidad.", "Docker Engine (app/Dockerfile)", "Amazon ECR + AWS Fargate"),
        ("Balanceador", "Reparte las peticiones entre réplicas. Detecta instancias no saludables y aísla degradaciones.", "NGINX 1.30 (proxy inverso Capa 7)", "AWS Application Load Balancer (ALB)"),
        ("Orquestador", "Garantiza el estado deseado ('quiero N réplicas'). Revive contenedores y gestiona despliegues seguros.", "Kubernetes Deployment (k8s/app.yaml)", "Amazon ECS Service + Circuit Breaker"),
        ("Clúster", "Agrupa múltiples máquinas (nodos) para que la caída de un servidor físico no detenga el servicio.", "Kind (3 nodos: 1 control + 2 workers)", "Infraestructura AWS Multi-AZ (Fargate)")
    ]

    for i, fila in enumerate(filas_piezas):
        row = tbl_piezas.rows[i+1]
        for j, val in enumerate(fila):
            cell = row.cells[j]
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9)
            if i % 2 == 1:
                set_cell_background(cell, "F6F8FB")

    # ========================== 3. GUIA 1 LOCAL ==========================
    doc.add_page_break()
    h1 = doc.add_heading("3. DESARROLLO EXPERIMENTAL: GUÍA 1 (LOCAL)", level=1)
    h1.runs[0].font.color.rgb = NAVY
    h1.runs[0].font.bold = True

    h2 = doc.add_heading("3.1 Parte A · Contenedor Único y Análisis de Estado (A1 – A3)", level=2)
    h2.runs[0].font.color.rgb = DARK

    doc.add_paragraph(
        "Se construyó la imagen Docker lab-fallas:1.0 a partir del código FastAPI. Se ejecutó un contenedor único expuesto en el puerto 8000.\n"
        "• Experimento A1: Al enviar peticiones consecutivas, la misma réplica atiende y su contador local incrementa progresivamente (1 -> 2 -> 3).\n"
        "• Experimento A2 (Punto Único de Falla): Se invocó POST /crash (os._exit(1)). El contenedor colapsó de inmediato (Exited (1)). Al carecer de orquestador o balanceador, el servicio quedó 100% indisponible ante los usuarios.\n"
        "• Experimento A3 (Política de Reinicio): Al agregar --restart unless-stopped, Docker detectó la caída y reinició el contenedor en 2 segundos. Sin embargo, al consultar GET /, el contador volvió a empezar en 1. Esto comprobó el axioma arquitectónico: 'Lo que vive en memoria RAM del contenedor muere con él. Reiniciar no previene la pérdida de datos'."
    )

    def add_fig(img_rel, caption, width=Inches(5.5)):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, img_rel)
        if os.path.exists(full_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_picture(full_path, width=width)
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_cap = p_cap.add_run(caption)
            r_cap.font.size = Pt(8.5)
            r_cap.font.italic = True

    h2 = doc.add_heading("3.2 Parte B · Réplicas, NGINX y Persistencia con Redis (B1 – B4)", level=2)
    h2.runs[0].font.color.rgb = DARK

    doc.add_paragraph(
        "Mediante Docker Compose se orquestaron 3 réplicas de la API, un balanceador NGINX en Capa 7 y un motor Redis para persistencia de estado.\n"
        "• B1 (Round Robin): NGINX distribuyó las peticiones equitativamente entre las 3 réplicas. El monitor visual confirmó cuadros de 3 colores alternándose.\n"
        "• B2 (Tolerancia a Caídas: NGINX Bueno vs. Defectuoso): Se eliminó una réplica con 'docker kill lab-fallas-api-2'. Con nginx.conf configurado con 'max_fails=1' y 'proxy_next_upstream error timeout', se logró 0% de error visible: NGINX redirigió en milisegundos las peticiones a las réplicas sanas. En contraste, con nginx-defectuoso.conf (sin reintentos y max_fails=0), el usuario recibió un 33.7% de errores HTTP 504 Gateway Timeout (cuadritos rojos en el monitor).\n"
        "• B3 (Estado Compartido en Redis): Al inyectar REDIS_URL=redis://redis:6379/0, el contador dejó de ser local a cada contenedor y pasó a ser centralizado. La secuencia fue rigurosamente continua (1, 2, 3... 100) entre las diferentes réplicas.\n"
        "• B4 (Mitigación de Réplicas Lentas): Se inyectó latencia de 2 segundos mediante POST /lento. Con Round Robin, la réplica lenta siguió recibiendo el 35.3% del tráfico a pesar de tardar 2063 ms. Al activar 'least_conn;', NGINX redujo drásticamente el tráfico hacia dicha instancia (cayendo a un 1.9%), desviando el 98.1% hacia las réplicas sanas."
    )

    # Insertar capturas del monitor Parte B
    add_fig("docs/evidencias/monitor_B1_round_robin.png", "Figura 1: Monitor visual en Experimento B1: Round Robin con 3 réplicas alternándose equitativamente (0 errores).")
    add_fig("docs/evidencias/monitor_B2a_failover_exitoso.png", "Figura 2: Monitor visual en Experimento B2(a): Failover exitoso con NGINX bueno tras 'docker kill lab-fallas-api-2' (0 errores).")
    add_fig("docs/evidencias/monitor_B2b_nginx_defectuoso_rojos.png", "Figura 3: Monitor visual en Experimento B2(b): Configuración defectuosa sin reintentos; se observan 34 cuadros rojos (33.7% error 504).")
    add_fig("docs/evidencias/monitor_B3_redis_compartido.png", "Figura 4: Monitor visual en Experimento B3: Persistencia centralizada con Redis; secuencia de contador global e incremental continua.")
    add_fig("docs/evidencias/monitor_B4a_lenta_round_robin.png", "Figura 5: Monitor visual en Experimento B4(a): Réplica lenta bajo Round Robin (recibe ~35% del tráfico a 2063 ms).")
    add_fig("docs/evidencias/monitor_B4b_lenta_least_conn.png", "Figura 6: Monitor visual en Experimento B4(b): Réplica lenta bajo Least Connections (tráfico redirigido al 98% a réplicas sanas).")

    # Insertar gráfico de algoritmos
    add_fig("docs/graficos/comparativa_algoritmos.png", "Figura 7: Distribución de tráfico en Experimento B4: Round Robin (ciego) vs. Least Connections (adaptativo).", width=Inches(5.8))

    h2 = doc.add_heading("3.3 Parte C · Clúster y Orquestación con Kubernetes Kind (C1 – C8)", level=2)
    h2.runs[0].font.color.rgb = DARK

    doc.add_paragraph(
        "Se desplegó un clúster Kubernetes local de 3 nodos (1 control-plane y 2 workers) con Kind:\n"
        "• C3 (Autocuración de Pods): Al ejecutar 'kubectl delete pod', el Deployment recreó inmediatamente una réplica sustituta en 4 segundos, conservando en todo momento el estado deseado (replicas: 3).\n"
        "• C4 (Crash de Proceso): Al tumbar el proceso con POST /crash, kubelet reinició el contenedor registrando RESTARTS=1. A diferencia de NGINX, el Service de Kubernetes (Capa 4) no reintenta peticiones en vuelo, evidenciando la necesidad de balanceadores Capa 7 en el borde.\n"
        "• C5 (Escalabilidad Elástica): Se escaló a 5 réplicas con 'kubectl scale'. El Service de Kubernetes descubrió dinámicamente los 2 nuevos pods sin requerir modificación alguna de archivos de configuración.\n"
        "• C6 (Caída de Nodo Completo): Se detuvo el contenedor de nodo 'ais86-worker' (simulando corte de energía de un servidor físico). Al expirar la tolerancia (15 segundos), el plano de control marcó el nodo como NotReady y reprogramó automáticamente los pods afectados en el nodo worker2, restableciendo el 100% de la capacidad operativa.\n"
        "• C7 (Despliegue Roto y Rollback): Se inyectó ROMPER_HEALTH=1. El pod nuevo nunca alcanzó el estado Ready (0/1) debido al fallo de readinessProbe. Kubernetes impidió la sustitución de los 3 pods antiguos, garantizando cero tiempo fuera de servicio hasta que se ejecutó 'kubectl rollout undo'."
    )

    # ========================== 4. GUIA 2 AWS ==========================
    doc.add_page_break()
    h1 = doc.add_heading("4. DESARROLLO EXPERIMENTAL: GUÍA 2 (AWS CLOUD)", level=1)
    h1.runs[0].font.color.rgb = NAVY
    h1.runs[0].font.bold = True

    doc.add_paragraph(
        "En la sesión de nube se replicaron los mismos principios de arquitectura utilizando servicios completamente administrados en AWS (Región us-east-2, Ohio):\n"
        "• Amazon ECR: Repositorio privado donde se publicó la imagen 280161530063.dkr.ecr.us-east-2.amazonaws.com/lab-fallas:1.0.\n"
        "• AWS Fargate: Capa de cómputo serverless donde las tareas se ejecutan sin aprovisionar máquinas virtuales EC2 (0.25 vCPU y 0.5 GB RAM).\n"
        "• Amazon ECS: Orquestador encargado de mantener las 2 tareas deseadas y supervisar su ciclo de vida.\n"
        "• Application Load Balancer (ALB): Balanceador Capa 7 de alta disponibilidad que expone el puerto 80 hacia el Target Group 'lab-fallas-tg' en el puerto 8000."
    )

    h2 = doc.add_heading("4.1 Demostración de los 3 Puntos de Control Exigidos", level=2)
    h2.runs[0].font.color.rgb = DARK

    doc.add_paragraph(
        "✅ PUNTO DE CONTROL 1: Disponibilidad y Balanceo en la Nube\n"
        "Se configuró el ALB (lab-fallas-alb-154417865.us-east-2.elb.amazonaws.com) conectado al Target Group 'lab-fallas-tg'. "
        "Las 2 tareas Fargate alcanzaron el estado 'healthy' superando el health check sobre /health. "
        "En el monitor visual (puerto 8090) se evidenció el balanceo equitativo de peticiones alternando 2 colores sin generar cuadros rojos."
    )

    # Insertar imagen de target group health check
    add_fig("docs/evidencias/aws_target_group_health_check.png", "Figura 8: Configuración validada de Health Checks en AWS Target Group (Ruta /health, umbral 2, intervalo 10s).", width=Inches(5.6))

    doc.add_paragraph(
        "✅ PUNTO DE CONTROL 2: Detección de Caída y Algoritmo de Menos Solicitudes Pendientes\n"
        "1. Caída de Tarea: Al invocar POST /crash, una de las tareas colapsó. ECS registró en la pestaña 'Events' la desvinculación inmediata "
        "(deregistered 1 targets) e inició una tarea de reemplazo (started 1 tasks: e4338c4507de...) para reponer el estado deseado en menos de 40 segundos.\n"
        "2. Cambio de Algoritmo: Con Round Robin y concurrencia de 8 hilos, la réplica lenta consumía el 50% de peticiones. Al modificar el algoritmo del Target Group "
        "a 'Least outstanding requests', el ALB redirigió automáticamente las solicitudes a la tarea sana disponible, disminuyendo radicalmente el impacto en latencia."
    )

    doc.add_paragraph(
        "✅ PUNTO DE CONTROL 3: Protección de Despliegue con Circuit Breaker y Rollback Automático\n"
        "Al generar una nueva revisión de la definición de tarea con ROMPER_HEALTH=1, las tareas nuevas arrancaron respondiendo código HTTP 500 en /health. "
        "El ALB las catalogó como 'unhealthy'. Al acumularse 3 tareas fallidas consecutivas (umbral mínimo del Circuit Breaker), Amazon ECS declaró "
        "la implementación como FAILED y activó el Rollback automático hacia la revisión funcional previa. Durante todo el proceso de fallo, "
        "las tareas originales continuaron sirviendo el tráfico y el monitor visual permaneció libre de cuadros rojos, demostrando protección total al cliente final."
    )

    # Insertar imagen de monitor visual
    add_fig("docs/evidencias/monitor_errores_red.png", "Figura 9: Diagnóstico en Monitor Visual: Detección gráfica en tiempo real de peticiones HTTP y registro de errores de red.", width=Inches(5.4))

    h2 = doc.add_heading("4.2 Análisis de Capacidad y Ley de Little (Prueba Opcional C4)", level=2)
    h2.runs[0].font.color.rgb = DARK

    doc.add_paragraph(
        "Para modelar la saturación de recursos en AWS Fargate, se diseñó e implementó el script 'capacidad.py'. "
        "El principio formal de colas responde a la Ley de Little: L = λ × W, donde los clientes en vuelo (L) equivalen "
        "a la tasa de peticiones atendidas por segundo (λ) multiplicada por el tiempo promedio de residencia o latencia (W). "
        "Al elevar los clientes simultáneos de 5 a 20 sobre una única tarea Fargate de 0.25 vCPU, la CPU se saturó cerca del 100%, "
        "provocando que la tasa (req/s) se mantuviera plana (~325 req/s) mientras la latencia p50 creció de 3 ms a 35 ms y la p95 a 72 ms. "
        "Al escalar a 4 tareas, la capacidad elástica absorbió la carga reduciendo la latencia a solo 3 ms."
    )

    add_fig("docs/graficos/ley_de_little_escalabilidad.png", "Figura 10: Curva empírica de degradación de latencia según Ley de Little en Fargate (1 Tarea saturada vs. 4 Tareas escaladas).", width=Inches(5.5))

    # ========================== 5. TABLA OFICIAL ==========================
    doc.add_page_break()
    h1 = doc.add_heading("5. MATRIZ OFICIAL DE RESULTADOS Y EVIDENCIAS REALES", level=1)
    h1.runs[0].font.color.rgb = NAVY
    h1.runs[0].font.bold = True

    doc.add_paragraph(
        "A continuación se presenta la matriz oficial consolidada del laboratorio con los resultados obtenidos en las terminales y consolas de prueba:"
    )

    tbl_entrega = doc.add_table(rows=8, cols=4)
    tbl_entrega.alignment = WD_TABLE_ALIGNMENT.CENTER
    cols_h = ["Exp.", "Qué rompimos", "Qué vimos (Evidencia Real)", "Qué pieza lo resolvió y cómo"]
    for j, h in enumerate(cols_h):
        c = tbl_entrega.rows[0].cells[j]
        set_cell_background(c, "1D3B8F")
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.size = Pt(9)

    tbl_entrega.columns[0].width = Inches(0.8)
    tbl_entrega.columns[1].width = Inches(1.8)
    tbl_entrega.columns[2].width = Inches(2.3)
    tbl_entrega.columns[3].width = Inches(2.2)

    evidencias_filas = [
        ("A2–A3", "Contenedor único detenido con POST /crash.", 
         "A2: curl devolvió Empty reply y estado Exited (1).\nA3: Con --restart unless-stopped revivió en 2s, pero el contador se reinició en 1.", 
         "Política de reinicio de Docker Engine revivió el contenedor, demostrando que reiniciar no preserva memoria local."),
        ("B2", "Réplica detenida con NGINX bueno vs defectuoso.", 
         "NGINX bueno: 12 peticiones OK (HTTP 200), 0 errores.\nNGINX defectuoso: 4 fallas (HTTP 502/504), 33% de error visible.", 
         "Balanceador NGINX Capa 7 con max_fails=1 y proxy_next_upstream error timeout reintentó la petición en réplica sana."),
        ("B3", "Estado en RAM inconsistente vs Redis.", 
         "En RAM: contadores aislados 1,1,1, 2,2,2.\nCon Redis: secuencia continua 1 -> 9 compartida por las 3 réplicas.", 
         "Motor de estado compartido (Redis). La arquitectura se desacopló haciéndose stateless."),
        ("B4", "Réplica degradada con latencia de 2s.", 
         "Round Robin: la réplica lenta recibió 8/24 (33.3%) a 2004 ms.\nleast_conn: bajó a 1/24 (4.2%) y las rápidas atendieron 95.8%.", 
         "Algoritmo adaptativo (least_conn). Enruta hacia la réplica con menor cantidad de peticiones activas."),
        ("C3–C4", "Pod borrado y proceso crasheado en Kubernetes.", 
         "C3: Reemplazo creado en 4s con nueva IP.\nC4: kubelet reinició contenedor (RESTARTS: 1). Tráfico sin interrupción.", 
         "Orquestador Kubernetes (Deployment controller y kubelet) reconcilió el estado deseado replicas: 3."),
        ("C6", "Apagado total de un nodo worker físico.", 
         "A los 15s errores breves. A los 30s nodo NotReady. A los 45s los 5 pods operaban en worker2.", 
         "Clúster multinodo + Tolerations (15s). Reprogramó la carga en el nodo sano disponible."),
        ("C7", "Despliegue de versión rota (ROMPER_HEALTH=1).", 
         "Pod nuevo bloqueado en 0/1 Running con RESTARTS: 2. Los 3 pods sanos mantuvieron 12 OK y 0 errores.", 
         "ReadinessProbe + Rolling Update de Kubernetes. Impide retirar réplicas sanas si la nueva no pasa su health check.")
    ]

    for i, fila in enumerate(evidencias_filas):
        row = tbl_entrega.rows[i+1]
        for j, val in enumerate(fila):
            c = row.cells[j]
            p = c.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if i % 2 == 1:
                set_cell_background(c, "F6F8FB")

    # ========================== 6. CONCLUSIONES ==========================
    doc.add_page_break()
    h1 = doc.add_heading("6. CONCLUSIONES Y RESPUESTAS DE DEFENSA ANTE EL DOCENTE", level=1)
    h1.runs[0].font.color.rgb = NAVY
    h1.runs[0].font.bold = True

    h2 = doc.add_heading("6.1 Pregunta Final de la Guía", level=2)
    h2.runs[0].font.color.rgb = DARK
    doc.add_paragraph(
        "«En su sistema, ¿cuál de las fallas de hoy les dolería más y qué pieza de las cuatro la previene?»\n\n"
        "Respuesta del equipo:\n"
        "La falla más catastrófica en un entorno productivo de negocio es el despliegue inadvertido de una versión rota "
        "o la corrupción silenciosa de transacciones por pérdida de estado en memoria. La pérdida de servicio completa "
        "se previene mediante la sinergia de dos piezas fundamentales: el Orquestador con despliegues progresivos (Rolling Update / Circuit Breaker) "
        "que actúa como guardián mediante health checks (readinessProbe), impidiendo que una versión dañada reciba tráfico real; "
        "y el Balanceador de Carga Capa 7 (NGINX o AWS ALB) configurado con aislamiento de latencia (least_conn / least outstanding requests) "
        "y reintentos automáticos. Para los datos de usuario (carritos de compra, sesiones), la solución estructural es la eliminación "
        "absoluta del estado dentro de los contenedores mediante bases de datos y cachés distribuidas como Redis."
    )

    h2 = doc.add_heading("6.2 Protocolo de Limpieza y Control de Costos en la Nube", level=2)
    h2.runs[0].font.color.rgb = DARK
    doc.add_paragraph(
        "Dado que los balanceadores ALB y las tareas de Fargate facturan por hora de aprovisionamiento independientemente de su uso, "
        "se ejecutó el protocolo de destrucción controlada:\n"
        "1. Eliminación forzada del servicio ECS 'api'.\n"
        "2. Eliminación del Application Load Balancer 'lab-fallas-alb' y su Target Group 'lab-fallas-tg'.\n"
        "3. Supresión del clúster Fargate 'lab-fallas'.\n"
        "4. Detención del monitor local mediante 'docker compose --profile monitor down'.\n"
        "El costo global del laboratorio en AWS fue inferior a US$ 0.16 de los créditos educativos asignados."
    )

    output_path = "c:\\Users\\roger\\Downloads\\lab-fallas\\lab-fallas\\INFORME_LAB_S12_ROMPE_LA_ARQUITECTURA.docx"
    doc.save(output_path)
    print(f"Documento Word generado exitosamente en: {output_path}")

if __name__ == "__main__":
    create_report()
