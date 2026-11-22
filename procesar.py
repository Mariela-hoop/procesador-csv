"""Limpia un CSV de ventas y muestra estadísticas básicas.

Rutas configurables por variables de entorno:
  INPUT_PATH  -> CSV de entrada  (por defecto /data/input/ventas.csv)
  OUTPUT_PATH -> CSV de salida   (por defecto /data/output/ventas_limpio.csv)
"""
import os
import sys

import pandas as pd

INPUT_PATH = os.getenv("INPUT_PATH", "/data/input/ventas.csv")
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "/data/output/ventas_limpio.csv")


def limpiar(df: pd.DataFrame) -> pd.DataFrame:
    # Nombres de columna en minúscula y sin espacios
    df.columns = df.columns.str.strip().str.lower()
    # Quitar espacios en textos y normalizar mayúsculas
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()
    df["producto"] = df["producto"].str.title()
    # Tipos correctos
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce")
    df["precio"] = pd.to_numeric(df["precio"], errors="coerce")
    # Eliminar duplicados y filas incompletas
    df = df.drop_duplicates()
    df = df.dropna(subset=["fecha", "producto", "cantidad", "precio"])
    df["total"] = df["cantidad"] * df["precio"]
    return df


def main() -> int:
    if not os.path.isfile(INPUT_PATH):
        print(f"ERROR: no existe el archivo de entrada: {INPUT_PATH}", file=sys.stderr)
        return 1

    df = pd.read_csv(INPUT_PATH)
    filas_entrada = len(df)
    limpio = limpiar(df)

    os.makedirs(os.path.dirname(OUTPUT_PATH) or ".", exist_ok=True)
    limpio.to_csv(OUTPUT_PATH, index=False)

    print(f"Filas de entrada: {filas_entrada}")
    print(f"Filas limpias:    {len(limpio)}")
    print(f"Ventas totales:   {limpio['total'].sum():.2f}")
    print("Total por producto:")
    print(limpio.groupby("producto")["total"].sum().round(2).to_string())
    print(f"Archivo escrito en: {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
