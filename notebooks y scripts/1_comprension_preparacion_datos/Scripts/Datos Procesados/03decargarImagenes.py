import os
import shutil
import requests
from PIL import Image
from io import BytesIO
import csv

# Función para normalizar el nombre del producto a partir del nombre del archivo de imagen
def normalizar_nombre_imagen(nombre_archivo):
    base_nombre = nombre_archivo.split(' ')[0]
    # Eliminar puntos adicionales
    base_nombre = base_nombre.replace('..', '.')
    extension = os.path.splitext(nombre_archivo)[1]
    return base_nombre + extension

# Función para descargar y guardar la imagen
def descargar_imagen(url, nombre_archivo):
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        img = Image.open(BytesIO(respuesta.content))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img.save(nombre_archivo)
    else:
        print(f"Error al descargar {url}")

# Función para crear directorios basados en el supermercado y el nombre normalizado
def crear_directorios(supermercado, nombre_normalizado):
    path = os.path.join(supermercado, nombre_normalizado)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

# Función para procesar el archivo CSV y descargar las imágenes
def procesar_archivo_csv(nombre_archivo_entrada):
    with open(nombre_archivo_entrada, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo, delimiter=';')
        for fila in lector:
            supermercado = fila['Supermercado']
            nombre_producto = fila['Producto']
            nombre_normalizado = normalizar_nombre_imagen(nombre_producto)
            url = fila['URL de la imagen']
            path_directorio = crear_directorios(supermercado, nombre_normalizado)
            nombre_archivo_imagen = os.path.join(path_directorio, nombre_normalizado + '.jpg')
            descargar_imagen(url, nombre_archivo_imagen)

# Función principal que integra todas las funcionalidades
def main():
    nombre_archivo_entrada = '02productos_filtrados.csv'
    procesar_archivo_csv(nombre_archivo_entrada)

if __name__ == "__main__":
    main()
