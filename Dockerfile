# Base slim con versión fija
FROM python:3.12.7-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1) Dependencias primero: aprovecha la caché de capas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Usuario sin privilegios y carpetas de datos
RUN useradd --create-home --uid 10001 appuser \
    && mkdir -p /data/input /data/output \
    && chown -R appuser:appuser /data

# 3) Código al final (cambia más seguido)
COPY --chown=appuser:appuser procesar.py .

# Configuración externa (valores por defecto, sobrescribibles con -e)
ENV INPUT_PATH=/data/input/ventas.csv \
    OUTPUT_PATH=/data/output/ventas_limpio.csv

USER appuser

# CMD en forma exec
CMD ["python", "procesar.py"]
