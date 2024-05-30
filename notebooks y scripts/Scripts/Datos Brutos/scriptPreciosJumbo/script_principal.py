from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os
import logging
import sys
import time

def scrape_categoria(categoria, start_page, end_page):
    # Configurar opciones para evitar la caché del navegador y ejecutar en modo headless
    firefox_options = Options()
    firefox_options.set_preference("network.http.cache.offline-capacity", 0)
    firefox_options.set_preference("network.http.cache.size", 0)
    firefox_options.set_preference("network.http.cache.enabled", False)
    firefox_options.add_argument("--headless")

    # Configurar logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Iniciar el navegador con las opciones configuradas
    driver = webdriver.Firefox(options=firefox_options)
    actions = ActionChains(driver)

    # Verificar si el archivo ya existe
    file_exists = os.path.isfile('preciosJumbo.csv')

    # Abrir el archivo CSV en modo de agregar
    with open('preciosJumbo.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')

        # Si el archivo no existía, escribir la fila de encabezado
        if not file_exists:
            writer.writerow(["Categoria", "Producto", "Precio", "URL de la imagen", "Fecha y hora", "Página"])

        # Recorrer cada página de la categoría
        for page in range(start_page, end_page + 1):
            url = f'https://www.jumbo.com.ar/{categoria}?page={page}'
            logging.info(f"Accediendo a la URL: {url}")

            try:
                driver.get(url)
                time.sleep(3)  # Esperar un poco para que la página se cargue inicialmente
            except Exception as e:
                logging.error(f"Error al acceder a {url}: {e}")
                continue

            # Desplazar hacia abajo en la página varias veces para asegurar la carga completa
            for _ in range(3):
                actions.send_keys(Keys.END).perform()
                time.sleep(2)  # Esperar para que el contenido cargue

            try:
                # Esperar a que los elementos se carguen
                wait = WebDriverWait(driver, 15)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'vtex-product-summary-2-x-productBrand')))
            except Exception as e:
                logging.error(f"Error esperando los elementos en {url}: {e}")
                continue

            # Obtener el HTML de la página
            html_content = driver.page_source

            # Analizar el HTML con BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Buscar los nombres de los productos
            productos_nombres = soup.find_all('span', class_='vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body')

            # Buscar los precios de los productos
            productos_precios_contenedores = soup.find_all('div', class_='jumboargentinaio-store-theme-1dCOMij_MzTzZOCohX1K7w')

            # Buscar las imágenes de los productos
            productos_imagenes = soup.find_all('img', class_='vtex-product-summary-2-x-imageNormal vtex-product-summary-2-x-image')

            # Iterar sobre la lista de nombres, precios e imágenes de productos
            for producto_nombre, producto_precio_contenedor, producto_imagen in zip(productos_nombres, productos_precios_contenedores, productos_imagenes):
                if producto_nombre and producto_precio_contenedor and producto_imagen:
                    producto_nombre_texto = producto_nombre.text.strip()
                    producto_precio_texto = producto_precio_contenedor.text.strip()
                    producto_imagen_url = producto_imagen.get('src', '')

                    # Eliminar caracteres no numéricos y espacios del precio
                    precio_limpio = producto_precio_texto.replace('$', '').replace('.', '').replace(',', '.').strip()

                    # Convertir el precio de texto a tipo numérico (por ejemplo, float)
                    precio_numerico = float(precio_limpio)
        
                    # Obtener la fecha y hora actuales
                    ahora = datetime.now()
                    fecha_hora = ahora.strftime("%d/%m/%Y, %H:%M:%S")

                    # Escribir los datos en el archivo CSV
                    writer.writerow([categoria, producto_nombre_texto, precio_numerico, producto_imagen_url, fecha_hora, page])

            # Escribir una línea para separar las páginas
            writer.writerow([])

    # Cerrar el navegador
    driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python script_principal.py <categoria> <pagina_inicio> <pagina_fin>")
        sys.exit(1)

    categoria = sys.argv[1]
    pagina_inicio = int(sys.argv[2])
    pagina_fin = int(sys.argv[3])

    scrape_categoria(categoria, pagina_inicio, pagina_fin)
