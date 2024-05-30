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
import logging
import sys

def configurar_navegador():
    firefox_options = Options()
    firefox_options.set_preference("network.http.cache.offline-capacity", 0)
    firefox_options.set_preference("network.http.cache.size", 0)
    firefox_options.set_preference("network.http.cache.enabled", False)
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(options=firefox_options)
    return driver

def obtener_datos_producto(soup):
    productos_nombres = soup.find_all('span', class_='vtex-product-summary-2-x-productBrand')
    productos_precios_contenedores = soup.find_all('span', class_='valtech-carrefourar-product-price-0-x-currencyContainer')
    productos_imagenes = soup.find_all('img', class_='vtex-product-summary-2-x-imageNormal vtex-product-summary-2-x-image')
    return zip(productos_nombres, productos_precios_contenedores, productos_imagenes)

def limpiar_precio(precio_texto):
    precio_limpio = precio_texto.replace('$', '').replace('.', '').replace(',', '.').strip()
    return float(precio_limpio)

def escribir_csv(writer, categoria, producto_nombre_texto, precio_numerico, producto_imagen_url, fecha_hora, page):
    writer.writerow([categoria, producto_nombre_texto, precio_numerico, producto_imagen_url, fecha_hora, page])

def scrape_categoria(categoria, start_page, end_page):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    driver = configurar_navegador()
    file_exists = os.path.isfile('preciosCarrefour.csv')
    
    with open('preciosCarrefour.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        if not file_exists:
            writer.writerow(["Categoria", "Producto", "Precio", "URL de la imagen", "Fecha y hora", "Página"])

        for page in range(start_page, end_page + 1):
            url = f'https://www.carrefour.com.ar/{categoria}?page={page}'
            logging.info(f"Accediendo a la URL: {url}")
            try:
                driver.get(url)
                for _ in range(3):
                    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                    WebDriverWait(driver, 2).until(lambda d: d.execute_script('return document.readyState') == 'complete')
                wait = WebDriverWait(driver, 15)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'vtex-product-summary-2-x-productBrand')))
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                for producto_nombre, producto_precio_contenedor, producto_imagen in obtener_datos_producto(soup):
                    if producto_nombre and producto_precio_contenedor and producto_imagen:
                        producto_nombre_texto = producto_nombre.text.strip()
                        producto_precio_texto = producto_precio_contenedor.text.strip()
                        producto_imagen_url = producto_imagen.get('src', '')
                        fecha_hora = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
                        precio_numerico = limpiar_precio(producto_precio_texto)
                        escribir_csv(writer, categoria, producto_nombre_texto, precio_numerico, producto_imagen_url, fecha_hora, page)
                writer.writerow([])  # Línea para separar las páginas
            except Exception as e:
                logging.error(f"Error procesando la página {page} de {categoria}: {e}")

    driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python script_principal.py <categoria> <pagina_inicio> <pagina_fin>")
        sys.exit(1)

    categoria = sys.argv[1]
    pagina_inicio = int(sys.argv[2])
    pagina_fin = int(sys.argv[3])

    scrape_categoria(categoria, pagina_inicio, pagina_fin)
