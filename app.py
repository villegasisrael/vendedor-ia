from flask import Flask, request, jsonify
from utils import find_product_price, preprocess_message

app = Flask(__name__)

# Variable global para manejar sugerencias pendientes
pending_confirmation = {}

@app.route("/webhook", methods=["POST"])
def webhook():
    """Endpoint para procesar mensajes entrantes"""
    global pending_confirmation  # Variable global para sugerencias
    incoming_msg = request.json.get("Body")
    msg_type = request.json.get("Type", "text")

    if msg_type == "text":
        # Si el mensaje es una confirmación de una sugerencia
        if incoming_msg.lower() == "sí" and pending_confirmation:
            # Procesar el producto sugerido
            product_name = pending_confirmation.get("suggested_product")
            response = find_product_price(product_name)
            pending_confirmation = {}  # Limpiar la sugerencia pendiente
            return jsonify({"response": response})

        elif incoming_msg.lower() == "no" and pending_confirmation:
            # Cancelar la sugerencia
            pending_confirmation = {}
            return jsonify({"response": "Entendido. Por favor, intenta describir el producto nuevamente."})

        # Procesar el mensaje normalmente
        processed_msg = preprocess_message(incoming_msg)
        response = find_product_price(processed_msg)

        # Si el mensaje contiene una sugerencia
        if response.startswith("¿Quisiste decir"):
            suggested_product = response.split("'")[1]  # Extraer el producto sugerido
            pending_confirmation = {"suggested_product": suggested_product}
            return jsonify({"response": response})

        # Respuesta normal
        return jsonify({"response": response})

    else:
        # Mensaje no procesable (audio, imágenes, etc.)
        return jsonify({"response": "Por ahora solo puedo procesar mensajes de texto."})


if __name__ == "__main__":
    app.run(debug=True)
