import csv
from collections import defaultdict

def leer_archivo(nombre_archivo):
    datos = defaultdict(list)
    nombre_supermercado = obtener_nombre_supermercado(nombre_archivo)
    
    with open(nombre_archivo, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo, delimiter=';')
        encabezados = lector.fieldnames
        for fila in lector:
            fila_normalizada = normalizar_fila(fila, encabezados)
            categoria = fila_normalizada['Categoria']
            producto = fila_normalizada['Producto']
            precio = fila_normalizada['Precio'].strip()
            url = fila_normalizada['URL']
            fecha = fila_normalizada['Fecha y hora']
            if precio and precio != 'N/A':
                # Verificar si ya existe una entrada para este producto
                encontrado = False
                for registro in datos[producto]:
                    if registro['Categoria'] == categoria and registro['Precio'] == precio and registro['URL'] == url:
                        encontrado = True
                        break
                if not encontrado:
                    datos[producto].append({
                        'Supermercado': nombre_supermercado,
                        'Categoria': categoria,
                        'Producto': producto,
                        'Precio': precio,
                        'URL': url,
                        'Fecha': fecha
                    })
    return datos

def obtener_nombre_supermercado(nombre_archivo):
    if 'Carrefour' in nombre_archivo:
        return 'Carrefour'
    elif 'Jumbo' in nombre_archivo:
        return 'Jumbo'
    elif 'LaAnonima' in nombre_archivo:
        return 'La Anonima'
    else:
        return 'Desconocido'

def normalizar_fila(fila, encabezados):
    # Normalizar los nombres de las columnas
    campos_normalizados = {
        'Categoria': 'Categoria',
        'Producto': 'Producto',
        'Precio': 'Precio',
        'URL': 'URL',
        'Fecha y hora': 'Fecha y hora'
    }
    fila_normalizada = {}
    for encabezado in encabezados:
        encabezado_normalizado = campos_normalizados.get(encabezado, encabezado)
        fila_normalizada[encabezado_normalizado] = fila[encabezado]
    return fila_normalizada

def escribir_archivo_modificado(datos, nombre_archivo):
    fieldnames = ['Supermercado', 'Categoria', 'Producto', 'Precio', 'URL', 'Fecha']
    
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=fieldnames, delimiter=';')
        escritor.writeheader()
        
        for producto, registros in datos.items():
            for registro in registros:
                escritor.writerow(registro)

def main():
    archivos = [
        'frutasyverduras.csv'
    ]
    datos_totales = defaultdict(list)
    
    for archivo in archivos:
        datos = leer_archivo(archivo)
        for producto, registros in datos.items():
            datos_totales[producto].extend(registros)

    # Eliminar duplicados globales
    datos_depurados = defaultdict(list)
    datos_repetidos = defaultdict(list)
    
    for producto, registros in datos_totales.items():
        unique_records = []
        for registro in registros:
            if registro not in unique_records:
                unique_records.append(registro)
        if len(unique_records) > 1:
            datos_repetidos[producto] = unique_records
        else:
            datos_depurados[producto] = unique_records
    
    escribir_archivo_modificado(datos_depurados, '01_salida_productos_depuradosporCategoria.csv')
    escribir_archivo_modificado(datos_repetidos, 'productos_repetidos_Todos.csv')

if __name__ == "__main__":
    main()
