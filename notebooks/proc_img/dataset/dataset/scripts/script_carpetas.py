import os
import shutil

# Directorio raíz donde están los supermercados
root_dir = 'C:/Users/Usuario/OneDrive/Desktop/asistente-de-compras/dataset'

# Obtener la lista de supermercados
supermarkets = os.listdir(root_dir)

# Iterar sobre cada supermercado
for supermarket in supermarkets:
    supermarket_dir = os.path.join(root_dir, supermarket)
    
    if os.path.isdir(supermarket_dir):
        # Obtener la lista de archivos de imagen en el supermercado
        images = os.listdir(supermarket_dir)
        
        for image in images:
            if image.endswith('.jpg'):  # Asegúrate de que es un archivo de imagen
                # Nombre del producto (sin la extensión)
                product_name = os.path.splitext(image)[0]
                
                # Crear la carpeta del producto
                product_dir = os.path.join(supermarket_dir, product_name)
                os.makedirs(product_dir, exist_ok=True)
                
                # Mover la imagen a la carpeta del producto
                source_file = os.path.join(supermarket_dir, image)
                destination_file = os.path.join(product_dir, image)
                shutil.move(source_file, destination_file)

print("Imágenes organizadas en carpetas por producto.")
