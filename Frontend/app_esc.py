import streamlit as st
import requests
from PIL import Image
import io

# Configuración de la página
st.set_page_config(page_title="NeumDetect", layout="wide")

# Funciones de predicción para cada modelo
def predict_vgg16(image):
    return send_prediction_request(image, "vgg16")

def predict_resnet50(image):
    return send_prediction_request(image, "resnet50")

def predict_custom(image):
    return send_prediction_request(image, "custom")

def send_prediction_request(image, model_name):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    files = {'file': ('image.png', img_byte_arr, 'image/png')}
    response = requests.post(f"http://localhost:8000/predict_{model_name}", files=files)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error al procesar la imagen con el modelo {model_name}. Por favor, intente de nuevo.")
        return None

# Diccionario de modelos disponibles
MODELS = {
    "Modelo VGG16": predict_vgg16,
    "Modelo ResNet50": predict_resnet50,
    "Modelo personalizado": predict_custom
}

# Título y logo
st.title("NeumDetect: Detección de Neumonía")
st.write("Plataforma de detección de neumonía basada en imágenes de rayos X de tórax")

# Carga de imagen
uploaded_file = st.file_uploader("Cargar imagen de rayos X", type=["jpg", "jpeg", "png"])

# Selección de modelo
model_choice = st.selectbox("Seleccionar modelo", list(MODELS.keys()))

# Botón para realizar la predicción
if st.button("Realizar predicción"):
    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        # Realizar predicción con el modelo seleccionado
        result = MODELS[model_choice](image)

        if result:
            col1, col2 = st.columns([1, 2])

            with col1:
                st.image(image, caption="Imagen cargada", width=300)

                st.write(f"Diagnóstico: {result['diagnosis']}")
                st.write(f"Probabilidad: {result['probability']}")
            # with col2:
    else:
        st.write("Por favor, carga una imagen antes de realizar la predicción.")
