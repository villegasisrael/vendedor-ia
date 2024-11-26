from flask import Flask, request, jsonify
from utils import find_product_price, preprocess_message
from classifier import classify_message

app = Flask(__name__)

# Variable global para manejar selección pendiente
pending_selection = {}

@app.route("/webhook", methods=["POST"])
def webhook():
    """Endpoint para procesar mensajes entrantes"""
    global pending_selection  # Manejar selección pendiente
    incoming_msg = request.json.get("Body")
    msg_type = request.json.get("Type", "text")

    if not incoming_msg:
        return jsonify({"response": "No se recibió ningún mensaje. Por favor, inténtalo de nuevo."})

    if msg_type == "text":
        # Si hay una selección pendiente
        if pending_selection:
            try:
                user_choice = int(incoming_msg.strip())
                response = find_product_price(product_name=None, user_selection=user_choice)
                pending_selection.clear()  # Limpiar selección pendiente después de usarla
                return jsonify({"response": response})
            except ValueError:
                return jsonify({"response": "Por favor, responde con el número de la opción que deseas."})

        # Procesar el mensaje normalmente
        processed_msg = preprocess_message(incoming_msg)
        category = classify_message(processed_msg)

        # Manejar categorías específicas
        if category == "soporte":
            return jsonify({"response": "Entendido, ¿qué problema tienes con tu producto?"})
        elif category == "producto":
            response = find_product_price(processed_msg)
            if "múltiples coincidencias" in response.lower():
                pending_selection["waiting_for_selection"] = True  # Marca selección pendiente
            return jsonify({"response": response})
        elif category == "otros":
            return jsonify({"response": "No estoy seguro de entender tu solicitud. Por favor, sé más específico."})

        # Respuesta genérica
        return jsonify({"response": "¿En qué más puedo ayudarte?"})

    else:
        # Mensaje no procesable (audio, imágenes, etc.)
        return jsonify({"response": "Por ahora solo puedo procesar mensajes de texto."})


if __name__ == "__main__":
    app.run(debug=True)
