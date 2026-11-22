# procesador-csv

Script en Python (pandas) que limpia un CSV de ventas: normaliza nombres de columnas y textos, convierte tipos, elimina duplicados y filas incompletas, calcula la columna `total` y muestra estadísticas. Empaquetado en Docker.

Imagen publicada: `docker.io/TU_USUARIO/procesador-csv:1.0.0`

## Requisitos
Solo Docker.

## Ejecutar desde Docker Hub (sin clonar nada)

```bash
mkdir -p datos/entrada datos/salida
# coloca tu CSV en datos/entrada/ventas.csv (o usa sample/ventas.csv de este repo)

docker run --rm \
  -v "$(pwd)/datos/entrada:/data/input:ro" \
  -v "$(pwd)/datos/salida:/data/output" \
  TU_USUARIO/procesador-csv:1.0.0
```

En PowerShell reemplaza `$(pwd)` por `${PWD}`.

## Construir localmente

```bash
docker build -t procesador-csv:1.0.0 .
docker run --rm \
  -v "$(pwd)/sample:/data/input:ro" \
  -v "$(pwd)/salida:/data/output" \
  procesador-csv:1.0.0
```

## Variables de entorno

| Variable | Por defecto | Descripción |
|---|---|---|
| `INPUT_PATH` | `/data/input/ventas.csv` | Ruta (dentro del contenedor) del CSV de entrada |
| `OUTPUT_PATH` | `/data/output/ventas_limpio.csv` | Ruta (dentro del contenedor) del CSV de salida |

Ejemplo con otro nombre de archivo:

```bash
docker run --rm -e INPUT_PATH=/data/input/enero.csv -e OUTPUT_PATH=/data/output/enero_limpio.csv \
  -v "$(pwd)/datos/entrada:/data/input:ro" -v "$(pwd)/datos/salida:/data/output" \
  TU_USUARIO/procesador-csv:1.0.0
```

## Puertos
No aplica (el contenedor no expone puertos).

## Volúmenes

| Ruta en el contenedor | Uso |
|---|---|
| `/data/input` | Entrada (montar en solo lectura) |
| `/data/output` | Salida (el CSV limpio se escribe aquí) |

## Ejemplo y salida esperada

Con `sample/ventas.csv` (7 filas con duplicado, vacíos y un precio inválido):

```
Filas de entrada: 7
Filas limpias:    4
Ventas totales:   19.40
Total por producto:
producto
Banano     6.0
Manzana    9.4
Pera       4.0
Archivo escrito en: /data/output/ventas_limpio.csv
```

Contenido de `ventas_limpio.csv`:

```
fecha,producto,cantidad,precio,total
2025-01-05,Manzana,10.0,0.5,5.0
2025-01-06,Pera,5.0,0.8,4.0
2025-01-08,Banano,20.0,0.3,6.0
2025-01-10,Manzana,8.0,0.55,4.4
```

## Problemas frecuentes
- **Permission denied al escribir la salida (Linux):** el contenedor corre como usuario no root (UID 10001). Ejecuta `chmod 777 datos/salida` o añade `--user $(id -u):$(id -g)` al `docker run`.
- **ERROR: no existe el archivo de entrada:** revisa que el CSV esté en la carpeta montada y que el nombre coincida con `INPUT_PATH`.
