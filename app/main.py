"""Servicio de laboratorio AIS86 S12: un servicio pequeño que se puede romper a propósito.

Endpoints:
  GET  /            responde quién atendió (réplica), su contador y la versión
  GET  /health      salud (falla a propósito si ROMPER_HEALTH=1)
  POST /crash       mata el proceso (simula una caída)
  POST /lento       activa/desactiva el modo lento en ESTA réplica
"""
import os
import socket
import time

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

VERSION = os.getenv("VERSION", "1.0")
REPLICA = socket.gethostname()
REDIS_URL = os.getenv("REDIS_URL")  # si existe, el contador vive FUERA del contenedor

app = FastAPI(title="lab-fallas")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

contador_local = 0  # estado guardado DENTRO de la réplica (el defecto a observar)
lento = False
redis_cli = None
if REDIS_URL:
    import redis

    redis_cli = redis.Redis.from_url(REDIS_URL)


def cerrar(resp: Response) -> None:
    # Cierra la conexión tras cada respuesta para que un balanceador de capa 4
    # (Kubernetes Service) reparta cada petición y no solo cada conexión.
    resp.headers["Connection"] = "close"


@app.get("/")
def raiz(resp: Response):
    global contador_local
    if lento:
        time.sleep(2)
    if redis_cli is not None:
        contador = int(redis_cli.incr("visitas"))
        origen = "redis (compartido)"
    else:
        contador_local += 1
        contador = contador_local
        origen = "memoria de la réplica"
    cerrar(resp)
    return {"replica": REPLICA, "contador": contador, "contador_en": origen, "version": VERSION, "lento": lento}


@app.get("/health")
def health(resp: Response):
    cerrar(resp)
    if os.getenv("ROMPER_HEALTH") == "1":
        resp.status_code = 500
        return {"ok": False, "replica": REPLICA}
    return {"ok": True, "replica": REPLICA}


@app.post("/crash")
def crash():
    os._exit(1)  # muerte abrupta, como un error fatal o falta de memoria


@app.post("/lento")
def toggle_lento(resp: Response):
    global lento
    lento = not lento
    cerrar(resp)
    return {"replica": REPLICA, "lento": lento}
