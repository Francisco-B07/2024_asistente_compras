import csv

def leer_archivo_simple(nombre_archivo):
    productos_urls = []
    with open(nombre_archivo, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo, delimiter=';')
        for fila in lector:
            producto = fila['Producto']
            url = fila['URL']
            if url:  # Verificar si la URL no está vacía
                productos_urls.append({'Producto': producto, 'URL': url})
    return productos_urls

def escribir_archivo_simple(datos, nombre_archivo):
    fieldnames = ['Producto', 'URL']
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=fieldnames, delimiter=';')
        escritor.writeheader()
        for registro in datos:
            escritor.writerow(registro)

# Archivo generado en el proceso anterior
archivo_depurado = 'productos_depuradosporCategoria.csv'
archivo_salida = '03productos_y_urls.csv'

# Leer los datos del archivo depurado
datos = leer_archivo_simple(archivo_depurado)

# Escribir los datos simplificados en el archivo de salida
escribir_archivo_simple(datos, archivo_salida)
