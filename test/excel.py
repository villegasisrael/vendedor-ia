from pathlib import Path
import pandas as pd

# Ruta base del archivo que se está ejecutando
base_path = Path(__file__).resolve().parent

# Construye la ruta relativa para el archivo Excel
excel_path = base_path.parent / "productos.xlsx"

try:
    df = pd.read_excel(excel_path)
    print("Contenido del archivo Excel:")
    print(df)
except FileNotFoundError:
    print(f"No se encontró el archivo en la ruta: {excel_path}")
except Exception as e:
    print(f"Error inesperado: {e}")
