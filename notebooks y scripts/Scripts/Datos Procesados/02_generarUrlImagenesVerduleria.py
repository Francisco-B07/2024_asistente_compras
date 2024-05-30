import csv

def normalizar_nombre_producto(nombre_producto):
    # Aquí puedes definir cómo quieres normalizar el nombre del producto
    return nombre_producto.split(' ')[0]

def filtrar_productos(nombre_archivo_entrada, nombre_archivo_salida):
    with open(nombre_archivo_entrada, newline='', encoding='utf-8') as archivo_entrada, \
         open(nombre_archivo_salida, mode='w', newline='', encoding='utf-8') as archivo_salida:
        
        lector = csv.DictReader(archivo_entrada, delimiter=';')
        fieldnames = ['Supermercado', 'Producto', 'NombreNormalizado', 'Precio', 'URL de la imagen']
        escritor = csv.DictWriter(archivo_salida, fieldnames=fieldnames, delimiter=';')
        
        escritor.writeheader()
        
        for fila in lector:
            categoria = fila['Categoria'].lower()
            precio = fila['Precio']
            url = fila['URL de la imagen']
            
            if ('verdura' in categoria or 'frutas' in categoria) and precio and url.startswith('http'):
                nombre_normalizado = normalizar_nombre_producto(fila['Producto'])
                nuevo_registro = {
                    'Supermercado': fila['Supermercado'],
                    'Producto': fila['Producto'],
                    'NombreNormalizado': nombre_normalizado,
                    'Precio': precio,
                    'URL de la imagen': url
                }
                escritor.writerow(nuevo_registro)

def main():
    nombre_archivo_entrada = '01productos_unicos.csv'
    nombre_archivo_salida = '02productosFrutasVerdurasNormalizada'
    filtrar_productos(nombre_archivo_entrada, nombre_archivo_salida)

if __name__ == "__main__":
    main()

