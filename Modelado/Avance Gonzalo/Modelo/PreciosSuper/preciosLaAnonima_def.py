from selenium import webdriver
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# Configurar logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Inicializar el driver de Selenium (asegúrate de tener el webdriver correcto instalado)
driver = webdriver.Chrome()

# Definir las categorías y sus respectivas páginas y ubicaciones
categorias = {
    'frutas-y-verduras': (3, 'n1_7'),
}

# Crear el archivo CSV y escribir el encabezado
with open('preciosLaAnonima.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['Categoria', 'Producto', 'Precio', 'URL de la imagen', 'Fecha y hora', 'pagina'])

    # Recorrer cada categoría
    for categoria, (num_paginas, ubicacion_sector) in categorias.items():
        # Recorrer cada página de la categoría
        for page in range(1, num_paginas + 1):
            url = f'https://supermercado.laanonimaonline.com/{categoria}/{ubicacion_sector}/pag/{page}/'
            driver.get(url)

            # Esperar a que se cargue el contenido dinámico
            wait = WebDriverWait(driver, 15)
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
                producto_imagen_url = producto_imagen.get('data-src')  # Utilizamos .get() para evitar errores

                # Obtener la fecha y hora actuales
                ahora = datetime.now()
                fecha_hora = ahora.strftime("%d/%m/%Y, %H:%M:%S")

                # Escribir los datos en el archivo CSV
                writer.writerow([categoria, producto_nombre_texto, producto_precio_texto, producto_imagen_url, fecha_hora, page])

# Cerrar el driver
driver.quit()
