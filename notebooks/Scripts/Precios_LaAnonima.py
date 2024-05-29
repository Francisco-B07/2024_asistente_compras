from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os

# Diccionario con las categorías y el rango de páginas a recorrer
categorias = {
    'almacen': [1, 54, 'n1_1'], 
    'bebidas': [1, 21, '/n1_2/'],
    'frescos': [1, 20, 'n1_6'],
    'congelados': [1, 5, 'n1_296'],
    'frutas-y-verduras': [1, 3, 'n1_7'],
    'carniceria': [1, 2, 'n1_8'],
    'perfumeria': [1, 38, 'n1_359'],
    'limpieza': [1, 19, 'n1_4'],
    'hogar': [1, 18, 'n1_9'],
    'vinos-finos': [1, 8, 'n2_37'],
}

# Iniciar el navegador
driver = webdriver.Firefox()

# Verificar si el archivo ya existe
file_exists = os.path.isfile('preciosLaAnonima.csv')

# Abrir el archivo CSV en modo de agregar
with open('preciosLaAnonima.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')

    # Si el archivo no existía, escribir la fila de encabezado
    if not file_exists:
        writer.writerow(["Categoria","Producto", "Precio", "URL de la imagen","Fecha y hora", "Página"])

    # Recorrer cada categoría
    for categoria, paginas in categorias.items():
        # Recorrer cada página de la categoría
        for page in range(paginas[0], paginas[1] + 1):
            url = f'https://supermercado.laanonimaonline.com/{categoria}/{paginas[2]}/pag/{page}/'
            driver.get(url)

        
            # Esperar a que se cargue el contenido dinámico
            wait = WebDriverWait(driver, 600)
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'precio')))

            # Obtener el HTML de la página
            html_content = driver.page_source

            # Analizar el HTML con BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Buscar todos los nombres de los productos
            productos_nombres = soup.find_all('a', id=lambda value: value and value.startswith("btn_nombre_imetrics_"))

            # Buscar todos los contenedores de precios de los productos
            productos_precios_contenedores = soup.find_all('div', class_='precio')

            # Buscar todas las imágenes de los productos
            productos_imagenes = soup.find_all('img', class_='imagenIz')

            # Iterar sobre la lista de nombres, precios e imágenes de productos
            for producto_nombre, producto_precio_contenedor, producto_imagen in zip(productos_nombres, productos_precios_contenedores, productos_imagenes):
                producto_nombre_texto = producto_nombre.text.strip()
                producto_precio_texto = producto_precio_contenedor.text.strip()
                producto_imagen_url = producto_imagen['src']

                  # Obtener la fecha y hora actuales
                ahora = datetime.now()
                fecha_hora = ahora.strftime("%d/%m/%Y, %H:%M:%S")

                # Escribir los datos en el archivo CSV
                writer.writerow([categoria, producto_nombre_texto, producto_precio_texto, producto_imagen_url, fecha_hora, page])

# Cerrar el navegador
driver.quit()








