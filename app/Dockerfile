# 1. Imagen base: Linux mínimo con Python
FROM python:3.12-slim
# 2. Carpeta de trabajo dentro de la imagen
WORKDIR /app
# 3. Primero las dependencias (cambian poco: se reutiliza la caché)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# 4. Luego el código (cambia mucho)
COPY main.py .
# 5. No correr como administrador
RUN useradd --create-home appuser
USER appuser
# 6. Qué puerto usa y qué proceso arranca al ejecutar el contenedor
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
