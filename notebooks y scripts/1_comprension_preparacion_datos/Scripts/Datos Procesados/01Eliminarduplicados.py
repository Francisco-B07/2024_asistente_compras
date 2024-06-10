import csv
from collections import defaultdict

def leer_archivo(nombre_archivo):
    datos = defaultdict(list)
    with open(nombre_archivo, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo, delimiter=';')
        for fila in lector:
            clave = (fila['Supermercado'], fila['Producto'])
            datos[clave].append(fila)
    return datos

def escribir_archivos(datos, nombre_archivo_unicos, nombre_archivo_duplicados):
    with open(nombre_archivo_unicos, mode='w', newline='', encoding='utf-8') as archivo_unicos, \
         open(nombre_archivo_duplicados, mode='w', newline='', encoding='utf-8') as archivo_duplicados:
        
        fieldnames = ['Categoria', 'Producto', 'Precio', 'URL de la imagen', 'Fecha y hora', 'Página', 'Supermercado']
        escritor_unicos = csv.DictWriter(archivo_unicos, fieldnames=fieldnames, delimiter=';')
        escritor_duplicados = csv.DictWriter(archivo_duplicados, fieldnames=fieldnames, delimiter=';')
        
        escritor_unicos.writeheader()
        escritor_duplicados.writeheader()
        
        for clave, registros in datos.items():
            if len(registros) > 1:
                for registro in registros:
                    escritor_duplicados.writerow(registro)
            else:
                escritor_unicos.writerow(registros[0])

def main():
    nombre_archivo = 'unificacionSupermercados.csv'
    datos = leer_archivo(nombre_archivo)
    escribir_archivos(datos, '01productos_unicos.csv', '01_01productos_duplicados.csv')

if __name__ == "__main__":
    main()
