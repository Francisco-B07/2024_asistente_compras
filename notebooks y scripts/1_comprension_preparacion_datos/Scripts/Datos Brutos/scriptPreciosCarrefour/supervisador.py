import os
import time
import csv
import logging
import subprocess
from concurrent.futures import ThreadPoolExecutor

def obtener_ultima_pagina_procesada(categoria):
    if not os.path.isfile('preciosCarrefour.csv'):
        return 0
    ultima_pagina = 0
    with open('preciosCarrefour.csv', 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            if row and row[0] == categoria:
                ultima_pagina = int(row[5])
    return ultima_pagina

def procesar_pagina(categoria, start_page, end_page):
    logging.info(f"Procesando categoría {categoria}, páginas {start_page} a {end_page}")
    subprocess.run(["python", "script_principal.py", categoria, str(start_page), str(end_page)])
    time.sleep(2)

def supervisar_progreso(categorias):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    with ThreadPoolExecutor(max_workers=5) as executor:  # Ajusta max_workers según la capacidad de tu máquina
        while categorias:
            futures = []
            for categoria, max_page in list(categorias.items()):
                ultima_pagina = obtener_ultima_pagina_procesada(categoria)
                if ultima_pagina < max_page:
                    start_page = ultima_pagina + 1
                    end_page = min(start_page + 1, max_page)
                    futures.append(executor.submit(procesar_pagina, categoria, start_page, end_page))
                else:
                    logging.info(f"Categoría {categoria} procesada completamente.")
                    categorias.pop(categoria)
            for future in futures:
                future.result()  # Espera a que todas las tareas terminen

if __name__ == "__main__":
    categorias = {
        'Electro-y-tecnologia/Informatica-y-gaming': 30,
        'Almacen/Aceites-y-vinagres': 6,
        'Almacen/Enlatados-y-Conservas': 14,
        'Almacen/Pastas-secas': 7,
        'Almacen/Arroz-y-legumbres': 7,
        'Almacen/Harinas': 6,
        'Almacen/Sal-aderezos-y-saborizadores': 18,
        'Almacen/Caldos-sopas-y-pure': 4,
        'Almacen/Reposteria-y-postres': 7,
        'Almacen/Snacks': 12,
        'Desayuno-y-merienda/Galletitas-bizcochitos-y-tostadas': 23,
        'Desayuno-y-merienda/Budines-y-magdalenas': 3,
        'Desayuno-y-merienda/Yerba': 5,
        'Desayuno-y-merienda/Cafe': 8,
        'Desayuno-y-merienda/Infusiones': 6,
        'Desayuno-y-merienda/Azucar-y-endulzantes': 5,
        'Desayuno-y-merienda/Mermeladas-y-otros-dulces': 11,
        'Desayuno-y-merienda/Cereales-y-barritas': 7,
        'Bebidas/Cervezas': 7,
        'Bebidas/Vinos': 22,
        'Bebidas/Fernet-y-aperitivos': 4,
        'Bebidas/Bebidas-blancas': 6,
        'Bebidas/Gaseosas': 6,
        'Bebidas/Aguas': 7,
        'Bebidas/Jugos': 10,
        'Bebidas/Bebidas-isotonicas': 2,
        'Bebidas/Bebidas-energizantes': 2,
        'Lacteos-y-productos-frescos/Leches': 5,
        'Lacteos-y-productos-frescos/Yogures': 10,
        'Lacteos-y-productos-frescos/Mantecas-margarinas-y-levaduras': 1,
        'Lacteos-y-productos-frescos/Dulce-de-leche': 2,
        'Lacteos-y-productos-frescos/Huevos': 1,
        'Lacteos-y-productos-frescos/Tapas-y-pastas-frescas': 6,
        'Lacteos-y-productos-frescos/Dulce-de-membrillo-y-otros-dulces': 1,
        'Lacteos-y-productos-frescos/Salchichas': 1,
        'Lacteos-y-productos-frescos/Quesos': 15,
        'Lacteos-y-productos-frescos/Fiambres': 6,
        'Frutas-y-Verduras': 7,
        'Elaboracion-carrefour': 1,
        'Panaderia/Panificados': 4,
        'Sandwiches-empanadas-y-tartas': 1,
        'Congelados/Hamburguesas': 4,
        'Congelados/Nuggets-y-rebozados': 9,
        'Congelados/Verduras-y-frutas': 1,
        'Congelados/Pollos': 1,
        'Limpieza/Limpieza-de-la-ropa': 12,
        'Limpieza/Insecticidas': 1,
        'Limpieza/Limpieza-de-pisos-y-muebles': 6,
        'Limpieza/Limpieza-de-cocina': 6,
        'Limpieza/Lavandinas': 2,
        'Limpieza/Rollos-de-cocina-y-servilletas': 2,
        'Limpieza/Desodorantes-de-ambiente': 9,
        'Limpieza/Articulos-de-limpieza': 14,
        'Perfumeria/Cuidado-de-la-piel': 14,
        'Perfumeria/Antitranspirantes-y-desodorantes': 8,
        'Perfumeria/Cuidado-corporal': 9,
        'Perfumeria/Algodones-e-hisopos': 2,
        'Perfumeria/Farmacia': 11,
        'Perfumeria/Proteccion-para-adultos': 2,
        'Perfumeria/Fragancias-y-maquillaje': 2,
        'Perfumeria/Cuidado-del-cabello': 49,
        'Perfumeria/Cuidado-dental': 12,
        'Perfumeria/Proteccion-femenina': 8,
        'Mascotas/Alimentos-para-perros': 12,
        'mascotas/accesorios-para-mascotas': 2,
        'Mascotas/Alimentos-para-gatos': 6,
        'bazar-y-textil/indumentaria': 50,
    }

    supervisar_progreso(categorias)
