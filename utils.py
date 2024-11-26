from fuzzywuzzy import process
from pathlib import Path
import pandas as pd
import unicodedata

# Variable para manejar la selección del usuario
pending_selection = {}

def normalize_text(text):
    """Normaliza el texto eliminando tildes, convirtiendo a minúsculas."""
    if not text:  # Si el texto es None o vacío, retorna una cadena vacía
        return ""
    text = text.lower()
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    return text

def preprocess_message(message):
    """Preprocesar el mensaje para manejar regionalismos y errores."""
    synonym_map = {
        "licuadora": ["licua", "licuaora", "batidora"],
        "precio": ["costo", "cuánto vale", "cuánto cuesta"],
        "no funciona": ["no sirve", "se apagó", "no enciende"],
        "hola": ["qué onda", "qué tal", "buenas"]
    }
    
    message = normalize_text(message)
    for key, synonyms in synonym_map.items():
        for synonym in synonyms:
            if synonym in message:
                message = message.replace(synonym, key)
    return message

def find_product_price(product_name=None, user_selection=None):
    """Busca el precio de un producto en el archivo Excel usando coincidencias aproximadas."""
    global pending_selection  # Para manejar selecciones de usuario

    # Ruta basada en el directorio desde donde se ejecuta el script
    base_path = Path.cwd()
    excel_path = base_path / "productos.xlsx"

    # Manejar selección de producto por parte del usuario
    if user_selection is not None and pending_selection:
        selected_index = int(user_selection) - 1  # Restar 1 porque las opciones son 1-based
        if 0 <= selected_index < len(pending_selection['matches']):
            product = pending_selection['matches'][selected_index]
            pending_selection = {}  # Limpiar la selección pendiente
            return f"El precio de {product['Nombre']} es ${product['Precio']:.2f}."
        else:
            return "Selección inválida. Por favor, intenta de nuevo."

    # Si no hay un producto específico, retorna un mensaje
    if not product_name:
        return "No se especificó ningún producto para buscar."

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
    matches = process.extract(product_name, nombres, limit=5)
    matches = [(match[0], match[1]) for match in matches if match[1] >= 40]

    # Filtrar las coincidencias que contienen el término buscado
    filtered_matches = [
        (name, score) for name, score in matches if product_name in name
    ]
    print(f"Coincidencias filtradas: {filtered_matches}")

    # Si hay múltiples coincidencias, sugerir opciones al usuario
    if len(filtered_matches) > 1:
        options = []
        for i, (name, score) in enumerate(filtered_matches):
            product = df[df['Nombre_Normalizado'] == name].iloc[0]
            options.append(f"{i+1}. {product['Nombre']} - ${product['Precio']:.2f}")
        
        pending_selection = {"matches": [df[df['Nombre_Normalizado'] == name].iloc[0] for name, _ in filtered_matches]}
        return "Encontré múltiples coincidencias:\n" + "\n".join(options) + "\nPor favor, responde con el número de la opción que deseas."

    # Si hay una única coincidencia aceptable
    if filtered_matches:
        best_match = filtered_matches[0][0]
        product = df[df['Nombre_Normalizado'] == best_match].iloc[0]
        return f"El precio de {product['Nombre']} es ${product['Precio']:.2f}."

    # Si no se encuentra ninguna coincidencia
    return "Lo siento, no encontré el producto que mencionas."