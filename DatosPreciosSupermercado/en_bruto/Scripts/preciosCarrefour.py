from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os

# Configurar opciones para evitar la caché del navegador
firefox_options = Options()
firefox_options.set_preference("network.http.cache.offline-capacity", 0)
firefox_options.set_preference("network.http.cache.size", 0)
firefox_options.set_preference("network.http.cache.enabled", False)

# Iniciar el navegador con las opciones configuradas
driver = webdriver.Firefox(options=firefox_options)


# Diccionario con las categorías y el rango de páginas a recorrer
categorias = {
    'almacen': [1, 50], #50
    #'Bazar-y-textil': [40, 50], #50
    #'Desayuno-y-merienda': [1, 50],#50
    #'Bebidas': [1, 50],#50
    #'Lacteos-y-productos-frescos': [21, 49],#49
    #'Carnes-y-Pescados': [1, 8],#8
    #'Frutas-y-Verduras': [1, 9],#9
    #'Panaderia': [1, 12],#12
    #'Limpieza': [43, 50],#50
    #'perfumeria': [1, 50],#50
    'Electro-y-tecnologia':[5, 5],#50
}

# Iniciar el navegador
driver = webdriver.Firefox()

# Verificar si el archivo ya existe
file_exists = os.path.isfile('preciosCarrefour.csv')

# Abrir el archivo CSV en modo de agregar
with open('preciosCarrefour.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')

    # Si el archivo no existía, escribir la fila de encabezado
    if not file_exists:
        writer.writerow(["Categoria","Producto", "Precio", "URL de la imagen","Fecha y hora"])

    # Recorrer cada categoría
    for categoria, paginas in categorias.items():
        # Recorrer cada página de la categoría
        for page in range(paginas[0], paginas[1] + 1):
            url = f'https://www.carrefour.com.ar/{categoria}?{page}'
            driver.get(url)
          
            # Desplazar hacia abajo en la página
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)

            wait = WebDriverWait(driver, 60)
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'vtex-product-summary-2-x-productBrand')))
            #element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'vtex-product-summary-2-x-brandName')))
            # Obtener el HTML de la página
            html_content = driver.page_source

            
            # Esperar a que la página se cargue completamente
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            # Obtener el HTML de la página
            html_content = driver.page_source

            # Analizar el HTML con BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Encontrar la etiqueta body
            body_tag = soup.find('body')

            # Navegar hasta el elemento con la clase "bg-base"
            elemento_bg_base = body_tag.find(class_='bg-base')

            # Buscar todos los nombres de los productos
            #productos_nombres = soup.find_all('span', class_=lambda x: x in ['vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body', 'vtex-product-summary-2-x-brandName t-body'])
            productos_nombres = soup.find_all('span', class_='vtex-product-summary-2-x-productBrand')
            
            # Buscar todos los contenedores de precios de los productos
           
            #productos_precios_contenedores = soup.find_all('span', class_='valtech-carrefourar-product-price-0-x-currencyContainer')
            # Buscar todas las imágenes de los productos
            productos_precios_contenedores = soup.find_all('span', class_='valtech-carrefourar-product-price-0-x-currencyContainer')
            #productos_imagenes = soup.find_all('img', class_='vtex-product-summary-2-x-imageNormal vtex-product-summary-2-x-image')
            
            #productos_imagenes = soup.find_all('img', class_='vtex-product-summary-2-x-imageNormal')
            productos_imagenes = soup.find_all('img', class_= 'vtex-product-summary-2-x-imageNormal vtex-product-summary-2-x-image') #, 'src': 'https://carrefourar.vtexassets.com/arquivos/ids/386717-170-170?v=638318705666830000&amp;width=170&amp;height=170&amp;aspect=true'})
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
