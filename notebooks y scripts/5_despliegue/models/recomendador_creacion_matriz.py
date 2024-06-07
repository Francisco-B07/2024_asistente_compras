
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


# IMPORTACIÓN DE DATOS
df = pd.read_csv("recomendacion_supermercado_id.csv")

# Creamos una matriz item-usuario solo con los datos necesarios
iu = df.pivot_table(index='UserID', columns='ClaveID', values='Quantity', fill_value=0)


# CÁLCULO DE LA SIMILITUD DE ITEMS
similitud_items = cosine_similarity(iu.to_numpy())

# CREACIÓN DE UNA MATRIZ DE RECOMENDACIONES
matriz_recomendaciones = pd.DataFrame(similitud_items, index=iu.index, columns=iu.index)

# Convertir el DataFrame de una matriz a un formato largo
matriz_recomendaciones_long = matriz_recomendaciones.stack().rename_axis(['id1', 'id2']).reset_index(name='similitud')
matriz_recomendaciones_long = matriz_recomendaciones_long[matriz_recomendaciones_long['id1'] != matriz_recomendaciones_long['id2']]
matriz_recomendaciones_long = matriz_recomendaciones_long[matriz_recomendaciones_long['id1'] < matriz_recomendaciones_long['id2']]

# Unir las imágenes de 'id2'
# matriz_recomendaciones_long = matriz_recomendaciones_long.join(images, on='id2')

# GUARDA LA MATRIZ DE RECOMENDACION A DISCO
matriz_recomendaciones_long.to_pickle("matriz_recomendaciones_long.pkl")



