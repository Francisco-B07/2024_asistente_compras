import csv
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Crear el nombre del archivo CSV con la fecha actual
nombre_archivo = datetime.now().strftime("%d%m%YpreciosLaAnonima2.csv")

# Inicializar el driver de Selenium (asegúrate de tener el webdriver correcto instalado)
driver = webdriver.Chrome()

# Definir las categorías y sus respectivas páginas y ubicaciones
categorias = {
    'almacen': (54, 'n1_1'), 
    'bebidas': (21, 'n1_2'),
    'frescos': (20, 'n1_6'),
    'congelados': (5, 'n1_296'),
    'frutas-y-verduras': (3, 'n1_7'),
    'carniceria': (2, 'n1_8'),
    'perfumeria': (38, 'n1_359'),
    'limpieza': (19, 'n1_4'),
    'hogar': (18, 'n1_9'),
    'vinos-finos': (8, 'n2_37'),
}

# Crear el archivo CSV y escribir el encabezado
with open(nombre_archivo, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['Categoria', 'Producto', 'Precio', 'URL de la imagen', 'Fecha y hora', 'Pagina'])

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

            # Buscar todos los productos
            productos = soup.find_all('div', class_='producto')

            # Iterar sobre cada producto
            for producto in productos:
                producto_nombre_elem = producto.find('a', id=lambda value: value and value.startswith("btn_nombre_imetrics_"))
                producto_precio_elem = producto.find('div', class_='precio')
                producto_imagen_elem = producto.find('img', class_='imagenIz')

                if producto_nombre_elem and producto_precio_elem and producto_imagen_elem:
                    producto_nombre_texto = producto_nombre_elem.text.strip()
                    producto_precio_texto = producto_precio_elem.text.strip()
                    producto_imagen_url = producto_imagen_elem['data-src'] if 'data-src' in producto_imagen_elem.attrs else producto_imagen_elem['src']

                    # Obtener la fecha y hora actuales
                    ahora = datetime.now()
                    fecha_hora = ahora.strftime("%d/%m/%Y, %H:%M:%S")

                    # Eliminar caracteres no numéricos y espacios del precio
                    precio_limpio = producto_precio_texto.replace('$', '').replace('.', '').replace(',', '.').strip()

                    try:
                        # Convertir el precio de texto a tipo numérico (por ejemplo, float)
                        precio_numerico = float(precio_limpio)
                    except ValueError:
                        logging.error(f'Error al convertir el precio: {producto_precio_texto}')
                        precio_numerico = 0.0

                    # Escribir los datos en el archivo CSV
                    writer.writerow([categoria, producto_nombre_texto, precio_numerico, producto_imagen_url, fecha_hora, page])

# Cerrar el driver
driver.quit()
