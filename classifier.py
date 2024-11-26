from transformers import pipeline

# Cargar modelo ajustado
classifier = pipeline(
    "text-classification",
    model="./modelo_clasificado",
    tokenizer="./modelo_clasificado",
    device=0  # Usar GPU si está disponible
)

# Mapeo de etiquetas (debe coincidir con las categorías del dataset)
label_mapping = {
    "LABEL_0": "otros",
    "LABEL_1": "producto",
    "LABEL_2": "soporte"
}

def classify_message(message):
    """Clasificar un mensaje"""
    result = classifier(message)
    print(f"Mensaje: {message}")
    print("Resultado de clasificación:", result)  # Para verificar la etiqueta y la confianza
    if result[0]["score"] > 0.4:
        label = result[0]["label"]
        return label_mapping.get(label, "otros")
    else:
        return "otros"

