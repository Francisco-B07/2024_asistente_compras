import csv
import os
import time
import subprocess
import concurrent.futures

def obtener_ultima_pagina_procesada(categoria):
    if not os.path.isfile('preciosJumbo.csv'):
        return 0

    ultima_pagina = 0
    with open('preciosJumbo.csv', 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            if row and row[0] == categoria:
                ultima_pagina = int(row[5])
    return ultima_pagina

def procesar_categoria(categoria, max_page):
    ultima_pagina = obtener_ultima_pagina_procesada(categoria)
    if ultima_pagina < max_page:
        start_page = ultima_pagina + 1
        end_page = min(start_page + 1, max_page)  # Ajusta este valor según el rendimiento deseado
        subprocess.run(["python", "script_principal.py", categoria, str(start_page), str(end_page)])
        time.sleep(10)  # Esperar 10 segundos antes de la próxima iteración
    else:
        print(f"Categoría {categoria} procesada completamente.")

def supervisar_progreso(categorias):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(procesar_categoria, categoria, max_page) for categoria, max_page in categorias.items()]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error procesando una categoría: {e}")

if __name__ == "__main__":
    categorias = {
        'Electro/Aire-Acondicionado-y-Ventilacion': 1,
        'Electro/audio': 2,
        'Electro/calefaccion-calefones-y-termotanques': 5,
        'Electro/Cocinas-y-Hornos': 1,
        'Electro/Consolas-y-Videojuegos': 1,
        'Electro/Heladeras-Freezers-y-Cavas': 2,
        'Electro/informatica': 3,
        'Electro/Lavado': 2,
        'Electro/Pequenos-Electros': 8,
        'electro/telefonos': 2,
        'electro/tv-y-video': 2,
        'Almacen/Aceites-y-Vinagres': 8,
        'Almacen/Aderezos': 9,
        'Almacen/Arroz-y-Legumbres': 4,
        'Almacen/Sal-Pimienta-y-Especias': 7,
        'Almacen/Conservas': 5,
        'Almacen/Desayuno-y-Merienda': 10,
        'Almacen/Golosinas-y-Chocolates': 17,
        'Almacen/harinas': 3,
        'Almacen/panificados': 5,
        'Almacen/caldos-sopas-pure-y-bolsas-para-horno': 4,
        'Almacen/para-preparar': 8,
        'Almacen/pastas-secas-y-salsas': 11,
        'Almacen/snacks': 9,
        'Bebidas/A-Base-de-Hierbas': 2,
        'Bebidas/Aguas': 5,
        'Bebidas/Aperitivos': 3,
        'Bebidas/Bebidas-Blancas': 3,
        'Bebidas/Cervezas': 8,
        'Bebidas/Champagnes': 3,
        'Bebidas/Energizantes': 1,  # Sin paginación específica, asumo 1 página
        'Bebidas/Jugos': 8,
        'Bebidas/Vinos': 31,
        'Bebidas/Whiskys': 3,
        'frutas-y-verduras/frutas': 7,
        'frutas-y-verduras/hierbas-aromaticas-y-plantines': 1,  # Sin paginación específica, asumo 1 página
        'frutas-y-verduras/huevos': 2,
        'frutas-y-verduras/legumbres-granos-y-semillas': 2,
        'frutas-y-verduras/organicos': 1,
        'carnes/carne-vacuna': 3,
        'carnes/carne-de-cerdo': 1,  # Sin paginación específica, asumo 1 página
        'carnes/cordero-lechon-chivito-y-conejo': 1,  # Sin paginación específica, asumo 1 página
        'carnes/carbon-y-lena': 2,
        'carnes/embutidos': 2,
        'carnes/pollos': 1,  # Sin paginación específica, asumo 1 página
        'Pescados-y-Mariscos/Pescados': 2,
        'Pescados-y-Mariscos/Mariscos': 2,
        'quesos-y-fiambres/quesos': 14,
        'quesos-y-fiambres/fiambres': 6,
        'quesos-y-fiambres/dulces': 1,
        'quesos-y-fiambres/encurtidos-aceitunas-y-pickles': 5,
        'quesos-y-fiambres/salchichas': 1,
        'lacteos/cremas': 1,
        'lacteos/dulce-de-leche': 1,
        'lacteos/leches': 4,
        'lacteos/mantecas-y-margarinas': 1,
        'lacteos/pastas-frescas-y-tapas': 5,
        'lacteos/postres': 1,
        'lacteos/yogures': 10,
        'Panaderia-y-Reposteria/Panaderia': 3,
        'Panaderia-y-Reposteria/Reposteria': 2,
        'Perfumeria/Cuidado-Capilar': 23,
        'Perfumeria/Cuidado-de-la-Piel': 8,
        'Perfumeria/Cuidado-Personal': 18,
        'Perfumeria/Cuidado-Oral': 8,
        'Perfumeria/Farmacia': 2,
        'limpieza/accesorios-de-limpieza': 7,
        'limpieza/calzado': 1,
        'limpieza/desodorantes-de-ambiente': 4,
        'limpieza/insecticidas': 2,
        'limpieza/lavandina': 2,
        'limpieza/limpieza-de-bano': 3,
        'limpieza/cuidado-para-la-ropa': 7,
        'limpieza/limpieza-de-cocina': 4,
        'limpieza/limpieza-de-pisos-y-muebles': 6,
        'limpieza/papeles': 3

    }

    supervisar_progreso(categorias)
