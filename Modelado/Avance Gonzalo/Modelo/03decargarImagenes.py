import requests
from PIL import Image
from io import BytesIO
import os
import re
from torchvision import ops  

def limpiar_nombre(nombre):
    # Eliminar caracteres no válidos del nombre del archivo
    return re.sub(r'[\\/:*?"<>|]', '_', nombre)

def descargar_imagen(url, nombre_archivo):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        if img.mode != 'RGB':
            img = img.convert('RGB')  # Convertir a modo RGB si no lo está
        img.save(nombre_archivo)
    else:
        print(f"Error al descargar {url}")

def preprocess_dataset(image, label):
    # Cambiar el tamaño de la imagen
    image = ops.image.resize(image, (INP_SIZE[0], INP_SIZE[1]))
    # Codificar las etiquetas en one-hot
    label = ops.one_hot(label, num_classes=2)
    return (image, label)

# Crear un directorio para guardar las imágenes
if not os.path.exists('imagenes_productos'):
    os.makedirs('imagenes_productos')

# Especifica la ruta completa al archivo CSV
archivo_csv = '03productos_y_urls.csv'

# Leer el archivo de productos y URLs
with open(archivo_csv, 'r', encoding='utf-8') as archivo:
    lineas = archivo.readlines()

# Descargar todas las imágenes
for linea in lineas[1:]:  # Saltar la cabecera
    producto, url = linea.strip().split(';')
    nombre_archivo = os.path.join('imagenes_productos', limpiar_nombre(producto) + '.jpg')
    descargar_imagen(url, nombre_archivo)
