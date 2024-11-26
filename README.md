
# Vendedor-IA

Vendedor-IA es un sistema basado en inteligencia artificial diseñado para interpretar y responder a mensajes de usuarios, con un enfoque en consultas de productos, servicios y soporte técnico. Este proyecto combina un modelo de lenguaje natural con un motor de búsqueda de productos, permitiendo manejar errores tipográficos y regionalismos de manera efectiva.

---

## **Características**
1. **Clasificación de Mensajes:**
   - Detecta si un mensaje está relacionado con productos, servicios, soporte técnico o temas generales.
   - Usa un modelo de lenguaje preentrenado en español y ajustado con datos específicos del dominio.

2. **Sugerencias para Coincidencias:**
   - Si no encuentra un producto exacto, sugiere al usuario una posible coincidencia y espera confirmación.

3. **Búsqueda de Productos:**
   - Consulta un catálogo de productos en un archivo Excel para devolver precios y descripciones.

4. **Procesamiento de Mensajes:**
   - Preprocesa mensajes para manejar sinónimos, errores tipográficos y expresiones regionales.

5. **Interfaz basada en API:**
   - Construida con Flask para manejar solicitudes entrantes desde integraciones como WhatsApp Business.

---

## **Requisitos del Sistema**
- Python 3.10 o superior.
- Dependencias listadas en `requirements.txt`.

---

## **Instalación**

### **1. Clonar el repositorio**
```bash
git clone https://github.com/usuario/vendedor-ia.git
cd vendedor-ia
```

### **2. Crear un entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

### **3. Instalar dependencias**
```bash
pip install -r requirements.txt
```

### **4. Configurar el proyecto**
Asegúrate de que los siguientes archivos estén en el directorio raíz del proyecto:

- `productos.xlsx`: Contiene el catálogo de productos.
- `responses.json`: Respuestas configuradas para categorías específicas.

---

### **Entrenamiento del Modelo**
1. **Preparar el Dataset**  
   - Asegúrate de que el archivo `dataset_ampliado.json` contiene ejemplos representativos de mensajes de tus usuarios, clasificados en las categorías `producto`, `soporte`, y `otros`.

2. **Entrenar el Modelo**  
   - Ejecuta el siguiente comando para entrenar el modelo:
   ```bash
   python train_model.py
   ```
   - Esto generará un modelo entrenado y lo almacenará en el directorio `modelo_clasificado/`.

---

## **Uso**

### **1. Iniciar el Servidor**
Ejecuta el servidor Flask con el siguiente comando:
```bash
python app.py
```

### **2. Probar la API**
Puedes usar **Postman**, **curl**, o cualquier cliente HTTP para enviar mensajes a la API.

#### **Ejemplo de Solicitud:**
- **URL:** `http://127.0.0.1:5000/webhook`
- **Método:** `POST`
- **Cuerpo:**
  ```json
  {
    "Body": "¿Qué precio tiene la licuadora básica?",
    "Type": "text"
  }
  ```

#### **Ejemplo de Respuesta:**
```json
{
  "response": "El precio de Licuadora Básica es $500.00."
}
```

---

## **Estructura del Proyecto**

```
vendedor-ia/
├── app.py               # Código principal de la aplicación Flask.
├── utils.py             # Funciones auxiliares (procesamiento de mensajes, búsqueda de productos).
├── classifier.py        # Clasificación de mensajes con modelo de lenguaje.
├── train_model.py       # Script para entrenar el modelo de clasificación.
├── transcriber.py       # (Opcional) Procesa mensajes de voz.
├── productos.xlsx       # Catálogo de productos con precios y descripciones.
├── dataset_ampliado.json# Dataset de entrenamiento para el modelo de clasificación.
├── responses.json       # Respuestas configuradas por categoría.
├── requirements.txt     # Dependencias necesarias para el proyecto.
├── modelo/              # (Opcional) Modelos preentrenados.
├── modelo_clasificado/  # (Opcional) Salida de entrenamiento.
├── test/                # Scripts para pruebas.
└── .gitignore           # Archivos y carpetas ignorados por Git.
```

---

## **Dependencias**
Estas son las dependencias necesarias para el proyecto, listadas en `requirements.txt`:

```
flask
transformers
datasets
accelerate
torch
pandas
fuzzywuzzy[speedup]
openpyxl
```

---

## **Próximos Pasos**
1. **Ampliar el Dataset**:
   - Recolectar mensajes reales de usuarios para mejorar el entrenamiento del modelo.
2. **Optimización de Coincidencias**:
   - Refinar el uso de fuzzy matching para mejorar las sugerencias.
3. **Integración con WhatsApp Business**:
   - Conectar el sistema con la API de WhatsApp Business para manejar mensajes en tiempo real.
4. **Mejorar la IA**:
   - Usar modelos más avanzados o entrenamiento específico para mejorar la comprensión del lenguaje natural.

---

## **Licencia**
Este proyecto está bajo la licencia MIT.

---

## **Contribuciones**
Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request para discutir posibles cambios.