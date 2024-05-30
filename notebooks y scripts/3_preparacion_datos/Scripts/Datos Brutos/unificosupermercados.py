import pandas as pd

# Nombres de los archivos CSV
archivos = [
    '290524preciosCarrefour.csv',
    '290524preciosLaAnonima.csv',
    '290524preciosJumbo.csv'
]

# Lista para almacenar los datos de todos los archivos
datos_unificados = []

# Definir los nombres de las columnas esperados
nombres_columnas = ['Categoria', 'Producto', 'Precio', 'URL de la imagen', 'Fecha y hora', 'Página']

for archivo in archivos:
    # Cargar el archivo CSV
    df = pd.read_csv(archivo, sep=';')
    
    # Normalizar los nombres de las columnas
    df.columns = [col.strip().replace(' ', '').capitalize() for col in df.columns]
    
    # Renombrar las columnas para que coincidan con los nombres esperados
    df.columns = nombres_columnas
    
    # Agregar el nombre del supermercado como primera columna
    df.insert(0, 'Supermercado', archivo[13:-4])  # Extrae el nombre del supermercado del nombre del archivo
    
    # Seleccionar solo las columnas deseadas para evitar duplicados
    df = df[nombres_columnas]
    df['Supermercado'] = archivo[13:-4]  # Añadir la columna del supermercado
    
    # Agregar el dataframe a la lista
    datos_unificados.append(df)

# Concatenar todos los dataframes
df_final = pd.concat(datos_unificados, ignore_index=True)

# Guardar el dataframe unificado en un nuevo archivo CSV
df_final.to_csv('unificacionSupermercados.csv', index=False, sep=';')
