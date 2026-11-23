#!/usr/bin/env python3
"""capacidad.py - Herramienta de prueba de capacidad para el laboratorio S12 AWS (C4)
Mide req/s, p50, p95 y errores contra el Application Load Balancer (ALB).
"""
import argparse
import csv
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor


def medir_cliente(url, duracion_segundos):
    latencias = []
    errores = 0
    codigos = {}
    fin = time.time() + duracion_segundos

    while time.time() < fin:
        t0 = time.perf_counter()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "capacidad/1.0", "Connection": "close"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                _ = resp.read()
                code = resp.status
        except urllib.error.HTTPError as e:
            code = e.code
            errores += 1
        except Exception:
            code = 0
            errores += 1

        t1 = time.perf_counter()
        latencias.append((t1 - t0) * 1000.0)  # ms
        codigos[code] = codigos.get(code, 0) + 1

    return latencias, errores, codigos


def correr_nivel(url, clientes, segundos):
    print(f"Probando {clientes} clientes simultaneos durante {segundos}s...", flush=True)
    t_inicio = time.time()
    todas_latencias = []
    total_errores = 0
    todos_codigos = {}

    with ThreadPoolExecutor(max_workers=clientes) as pool:
        futuros = [pool.submit(medir_cliente, url, segundos) for _ in range(clientes)]
        for f in futuros:
            lats, errs, cods = f.result()
            todas_latencias.extend(lats)
            total_errores += errs
            for c, cnt in cods.items():
                todos_codigos[c] = todos_codigos.get(c, 0) + cnt

    t_real = time.time() - t_inicio
    reqs = len(todas_latencias)
    rps = round(reqs / t_real, 1) if t_real > 0 else 0

    if todas_latencias:
        todas_latencias.sort()
        p50 = round(todas_latencias[int(len(todas_latencias) * 0.50)], 1)
        p95 = round(todas_latencias[int(len(todas_latencias) * 0.95)], 1)
    else:
        p50, p95 = 0, 0

    return {
        "clientes": clientes,
        "reqs": reqs,
        "rps": rps,
        "p50": p50,
        "p95": p95,
        "errores": total_errores,
        "codigos": todos_codigos
    }


def main():
    parser = argparse.ArgumentParser(description="Prueba de capacidad ALB - AIS86 UNAMBA")
    parser.add_argument("url", help="URL del servicio (ej. http://<DNS-del-ALB>/)")
    parser.add_argument("--segundos", type=int, default=30, help="Duracion por nivel (segundos, defecto: 30)")
    parser.add_argument("--etiqueta", type=str, default="1-tarea", help="Etiqueta para CSV (ej: 1-tarea, 4-tareas)")
    parser.add_argument("--niveles", type=str, default="5,10,20", help="Niveles de concurrencia separados por coma (ej: 5,10,20)")
    args = parser.parse_args()

    url = args.url.strip()
    if not url.endswith("/"):
        url += "/"

    niveles = [int(x.strip()) for x in args.niveles.split(",") if x.strip()]

    print(f"\n=======================================================")
    print(f"  AIS86 Lab S12 - Capacidad | Etiqueta: {args.etiqueta}")
    print(f"  Destino: {url}")
    print(f"=======================================================\n")

    # Probar conectividad antes
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "capacidad/1.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            print(f"[OK] Conectividad inicial exitosa (HTTP {r.status})\n")
    except Exception as e:
        print(f"[WARN] No se pudo verificar la URL inicialmente ({e}). Continuando...\n")

    resultados = []
    for c in niveles:
        res = correr_nivel(url, c, args.segundos)
        resultados.append(res)
        time.sleep(1)

    print("\n" + "="*65)
    print(f"{'Prueba':<12} {'Clientes':<10} {'req/s':<10} {'p50 (ms)':<12} {'p95 (ms)':<12} {'Errores':<8}")
    print("="*65)
    for r in resultados:
        print(f"{args.etiqueta:<12} {r['clientes']:<10} {r['rps']:<10} {r['p50']:<12} {r['p95']:<12} {r['errores']:<8}")
    print("="*65 + "\n")

    # Guardar en capacidad.csv
    csv_file = "capacidad.csv"
    existe = os.path.exists(csv_file)
    with open(csv_file, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not existe:
            writer.writerow(["etiqueta", "clientes", "req_s", "p50_ms", "p95_ms", "errores", "timestamp"])
        for r in resultados:
            writer.writerow([args.etiqueta, r["clientes"], r["rps"], r["p50"], r["p95"], r["errores"], time.strftime("%Y-%m-%d %H:%M:%S")])

    print(f"Resultados guardados en {csv_file}\n")


if __name__ == "__main__":
    main()
