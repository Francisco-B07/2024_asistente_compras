import csv
import os
import time
import subprocess
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Inicializar el driver de Selenium utilizando webdriver_manager para gestionar chromedriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Definir las categorías y sus respectivas páginas y ubicaciones
categorias = {
    #'almacen': (54, 'n1_1'), #
    #'bebidas': (21, 'n1_2'),
    #'frescos': (20, 'n1_6'),
    #'congelados': (5, 'n1_296'),
    'frutas-y-verduras': (3, 'n1_7'),
    #'carniceria': (2, 'n1_8'),
    #'perfumeria': (38, 'n1_359'),
    #'limpieza': (19, 'n1_4'),
    #'hogar': (18, 'n1_9'),
    #'vinos-finos': (8, 'n2_37'),
}

# Crear el archivo CSV y escribir el encabezado
with open('preciosLaAnonima.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['Categoria', 'Producto', 'Precio', 'URL de la imagen','Fecha y hora','pagina'])

    # Recorrer cada categoría
    for categoria, (num_paginas, ubicacion_sector) in categorias.items():
        # Recorrer cada página de la categoría
        for page in range(1, num_paginas + 1):
            url = f'https://supermercado.laanonimaonline.com/{categoria}/{ubicacion_sector}/pag/{page}/'
            driver.get(url)

            # Esperar a que se cargue el contenido dinámico
            wait = WebDriverWait(driver, 10)
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

            # Iterar sobre la lista de nombres, contenedores de precios e imágenes de productos
            for producto_nombre, producto_precio_contenedor, producto_imagen in zip(productos_nombres, productos_precios_contenedores, productos_imagenes):
                producto_nombre_texto = producto_nombre.text.strip()
                producto_precio_texto = producto_precio_contenedor.text.strip()
                producto_imagen_url = producto_imagen['data-src'] if 'data-src' in producto_imagen.attrs else producto_imagen['src']

                # Obtener la fecha y hora actuales
                ahora = datetime.now()
                fecha_hora = ahora.strftime("%d/%m/%Y, %H:%M:%S")

                # Escribir los datos en el archivo CSV
                writer.writerow([categoria, producto_nombre_texto, producto_precio_texto, producto_imagen_url,fecha_hora,page])

# Cerrar el driver
driver.quit()
