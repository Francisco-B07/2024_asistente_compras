import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
import numpy as np
import os
from translate import Translator

# Cargar el modelo preentrenado MobileNetV2
model = MobileNetV2(weights='imagenet')

# Inicializar el traductor
translator = Translator(to_lang="es")

def load_and_preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

def classify_image(img_path):
    img_array = load_and_preprocess_image(img_path)
    predictions = model.predict(img_array)
    decoded_predictions = decode_predictions(predictions, top=3)[0]
    return decoded_predictions

def translate_predictions(predictions):
    translated_predictions = []
    for pred in predictions:
        try:
            translated_text = translator.translate(pred[1])
            translated_predictions.append((translated_text, pred[2]))
        except Exception as e:
            print(f"Error translating {pred[1]}: {e}")
            translated_predictions.append((pred[1], pred[2]))
    return translated_predictions

def process_folder(folder_path):
    results = {}
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder_path, filename)
            predictions = classify_image(img_path)
            translated_predictions = translate_predictions(predictions)
            results[filename] = translated_predictions
    return results

# Ruta de la carpeta que contiene las imágenes
folder_path = 'prueba'

# Procesar las imágenes en la carpeta y obtener las predicciones
results = process_folder(folder_path)

# Mostrar los resultados
for filename, predictions in results.items():
    print(f"Imagen: {filename}")
    for pred in predictions:
        print(f"  - {pred[0]}: {pred[1]*100:.2f}%")
