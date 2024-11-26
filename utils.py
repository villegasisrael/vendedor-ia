from pathlib import Path
import pandas as pd
import unicodedata
from fuzzywuzzy import process  # Importar fuzzywuzzy para coincidencias aproximadas


def normalize_text(text):
    """Normaliza el texto eliminando tildes, convirtiendo a minúsculas."""
    text = text.lower()
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    return text


def preprocess_message(message):
    """Preprocesar el mensaje para manejar regionalismos y errores."""
    synonym_map = {
        "licuadora": ["licua", "licuaora", "batidora","Licuadora","licuadura"],
        "precio": ["costo", "cuánto vale", "cuánto cuesta","precio","acomo","a como"],
        "no funciona": ["no sirve", "se apagó", "no enciende"],
        "hola": ["qué onda", "qué tal", "buenas"]
    }
    
    message = normalize_text(message)
    for key, synonyms in synonym_map.items():
        for synonym in synonyms:
            if synonym in message:
                message = message.replace(synonym, key)
    return message


def find_product_price(product_name):
    """Busca el precio de un producto en el archivo Excel usando coincidencias aproximadas."""
    # Ruta basada en el directorio desde donde se ejecuta el script
    base_path = Path.cwd()  # Directorio de ejecución actual
    excel_path = base_path / "productos.xlsx"

    # Normalizar el texto del producto buscado
    product_name = normalize_text(product_name)
    print(f"Producto buscado (normalizado): {product_name}")

    # Cargar el archivo Excel
    try:
        df = pd.read_excel(excel_path)
        print(f"Contenido del Excel:\n{df}")
    except FileNotFoundError:
        return f"No se encontró el archivo en la ruta: {excel_path}"
    except Exception as e:
        return f"Error al leer el archivo: {e}"

    # Normalizar los nombres de los productos en el Excel
    df['Nombre_Normalizado'] = df['Nombre'].apply(normalize_text)
    print(f"Nombres normalizados en el Excel: {df['Nombre_Normalizado'].tolist()}")

    # Buscar el nombre más parecido usando fuzzy matching
    nombres = df['Nombre_Normalizado'].tolist()
    best_match, score = process.extractOne(product_name, nombres)
    print(f"Mejor coincidencia: {best_match} con puntaje: {score}")

    # Verificar la coincidencia
    if score >= 60:  # Coincidencia aceptable
        product = df[df['Nombre_Normalizado'] == best_match].iloc[0]
        return f"El precio de {product['Nombre']} es ${product['Precio']:.2f}."
    elif score >= 40:  # Coincidencia baja, preguntar al usuario
        return f"¿Quisiste decir '{best_match}'? Por favor confirma para darte el precio."
    else:  # Coincidencia muy baja
        return "Lo siento, no encontré el producto que mencionas."


