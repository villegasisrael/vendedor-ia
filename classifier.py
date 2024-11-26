from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

# Configurar dispositivo (GPU o CPU)
device = 0 if torch.cuda.is_available() else -1

# Ruta al modelo entrenado
model_name = "./modelo_clasificado"

# Inicializar el modelo y el tokenizador desde el modelo entrenado
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Crear el pipeline de clasificación
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, device=device)

# Mapeo de etiquetas del modelo a categorías entendibles
label_mapping = {
    "LABEL_0": "otros",
    "LABEL_1": "producto",
    "LABEL_2": "soporte"
}

def classify_message(message):
    """
    Clasifica un mensaje basado en las categorías del modelo entrenado.
    :param message: str - El mensaje de entrada a clasificar.
    :return: str - Categoría clasificada ('otros', 'producto', 'soporte').
    """
    # Clasificar el mensaje con el modelo
    result = classifier(message)
    print(f"Resultado de clasificación: {result}")  # Para depuración

    # Asegurar que la confianza sea suficiente
    if result[0]["score"] > 0.6:  # Ajusta este umbral según sea necesario
        return label_mapping.get(result[0]["label"], "otros")
    
    # Si la confianza no es suficiente, asignar 'otros'
    return "otros"
