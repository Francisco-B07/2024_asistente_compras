import pandas as pd
import datetime

# Función para leer los datasets
def cargar_datasets():
    productosCAR = pd.read_csv('productosCAR.csv', delimiter=';')
    productosJUM = pd.read_csv('productosJUM.csv', delimiter=';')
    productosLAN = pd.read_csv('productosLAN.csv', delimiter=';')
    return productosCAR, productosJUM, productosLAN

# Función para buscar el producto en los datasets
def buscar_producto(producto, datasets):
    resultados = []
    for nombre_ds, ds in datasets.items():
        coincidencias = ds[ds['Producto'].str.contains(producto, case=False, na=False)]
        for _, fila in coincidencias.iterrows():
            resultado = {
                'Supermercado': fila['Supermercado'],
                'Categoria': fila['Categoria'],
                'Producto': fila['Producto'],
                'Precio': fila['Precio'],
                'URL': fila['URL'],
                'Fecha': fila['Fecha'],
                'Fuente': nombre_ds
            }
            resultados.append(resultado)
    return resultados

# Función para registrar la consulta
def registrar_consulta(producto, resultados):
    with open('registro_consultas.csv', 'a') as f:
        for resultado in resultados:
            f.write(f"{datetime.datetime.now()};{producto};{resultado['Supermercado']};{resultado['Categoria']};{resultado['Producto']};{resultado['Precio']};{resultado['URL']};{resultado['Fecha']}\n")

def main():
    # Cargar datasets
    productosCAR, productosJUM, productosLAN = cargar_datasets()
    datasets = {'CAR': productosCAR, 'JUM': productosJUM, 'LAN': productosLAN}

    # Solicitar el producto al usuario
    producto = input("Ingrese el nombre del producto que desea buscar: ")

    # Buscar el producto en los datasets
    resultados = buscar_producto(producto, datasets)

    # Mostrar resultados
    if resultados:
        print(f"Resultados para '{producto}':")
        for resultado in resultados:
            print(f"Supermercado: {resultado['Supermercado']}, Producto: {resultado['Producto']}, Precio: {resultado['Precio']}, Fuente: {resultado['Fuente']}")
    else:
        print(f"No se encontraron resultados para '{producto}'.")

    # Registrar la consulta
    registrar_consulta(producto, resultados)

if __name__ == "__main__":
    main()
