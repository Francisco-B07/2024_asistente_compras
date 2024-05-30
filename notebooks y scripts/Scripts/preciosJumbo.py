from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os

# Diccionario con las categorías y el número de páginas a recorrer
categorias = {
    #'Almacen': [3, 50],  #[1, 50],
    #'bebidas': [1, 50],
    #'hogar-y-textil':[27, 50],
    #'frutas-y-verduras':[1, 17],
    #'carnes': [1, 8],
    'Quesos y Fiambres': [16, 24],
    'Lacteos': [1, 21],
    'perfumeria': [1, 50],
}

# Iniciar el navegador
driver = webdriver.Firefox()

# Verificar si el archivo ya existe
file_exists = os.path.isfile('preciosJumbo.csv')

# Conjunto para almacenar los productos ya escritos en el CSV
productos_ya_escritos = set()

# Si el archivo ya existe, leer los productos ya escritos
if file_exists:
    with open('preciosJumbo.csv', 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)  # Saltar la fila de encabezado
        for row in reader:
            if row:  # Ignorar filas vacías
                productos_ya_escritos.add(tuple(row[:-2]))  # Ignorar las columnas "Fecha y hora" y "Página"

# Abrir el archivo CSV en modo de agregar
with open('preciosJumbo.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    
    # Si el archivo no existía, escribir la fila de encabezado
    if not file_exists:
        writer.writerow(["Categoria","Producto", "Precio", "URL de la imagen","Fecha y hora", "Página"])

    # Recorrer cada categoría
    for categoria, paginas in categorias.items():
        # Recorrer cada página de la categoría
        for page in range(paginas[0], paginas[1] + 1):
            url = f'https://www.jumbo.com.ar/{categoria}?{page}'

            driver.get(url)

            # Esperar a que se cargue el contenido dinámico
            wait = WebDriverWait(driver, 30)
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'vtex-product-summary-2-x-productNameContainer')))

            # Obtener el HTML de la página
            html_content = driver.page_source

            # Analizar el HTML con BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Buscar todos los nombres de los productos
            productos_nombres = soup.find_all('span', class_='vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body')

            # Buscar todos los contenedores de precios de los productos
            productos_precios_contenedores = soup.find_all('div', class_='jumboargentinaio-store-theme-1dCOMij_MzTzZOCohX1K7w')

            # Buscar todas las imágenes de los productos
            productos_imagenes = soup.find_all('img', class_='vtex-product-summary-2-x-imageNormal vtex-product-summary-2-x-image')

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


        # Escribir una línea para separar las categorías
        writer.writerow([])

# Cerrar el navegador
driver.quit()
