# Librerías para reconocimiento de voz y procesamiento de audio
import speech_recognition as sr

# Librerías para manipulación de archivos y compresión

import os
import io

# Librerías para procesamiento de datos y análisis
import numpy as np
import pandas as pd
import spacy
import re
import nltk

# Descargar datos de WordNet si es necesario
nltk.download('wordnet')
from nltk.corpus import wordnet as wn

# Librería para generación de voz
from gtts import gTTS

# Importación de funciones comunes a otros cuadernos
from app.funciones_comunes import common_functions

# FAST API
from fastapi import APIRouter, HTTPException, Request, Form, Query, FastAPI, File, UploadFile
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
# from starlette.requests import Request
from pydub import AudioSegment

from typing import Dict

router = APIRouter()

# Configuración de las plantillas
templates = Jinja2Templates(directory="app/templates")


# ----------------LECTURA DE DATOS----------------
# DATOS FUENTES

# Cargar el modelo de spaCy para español
nlp = spacy.load("es_core_news_sm")

# Preprocesamiento de texto
# Lista de abreviaturas y formas no abreviadas de unidades de medida de peso
'''

# unidades_medida_peso = ['g', 'gr', 'kg', 'mg', 'µg', 't', 'lb', 'oz', 'cwt',
                        #'gramos', 'kilogramos', 'miligramos', 'microgramos',
                        #'toneladas', 'libras', 'onzas', 'quintales']

'''

# Lectura y almacenado del dataframe
path_csv_rutas_verduras = 'dataset/VerdurasporSupermercado.csv'
df_frutas_verduras = pd.read_csv(path_csv_rutas_verduras)


# CAPTURA DE AUDIO
async def entrada_voz(file: UploadFile = File(...)):
    recognizer = sr.Recognizer()  # Se inicializa el objeto de la clase speech recognition con el metodo recognizer y almacena en la variable 'recognizer'
    audio = AudioSegment.from_file(io.BytesIO(await file.read()), format="webm")
    audio = audio.set_frame_rate(16000)  # Asegúrate de que la tasa de muestreo sea compatible


    with io.BytesIO() as audio_file:
        audio.export(audio_file, format="wav")
        audio_file.seek(0)
        audio_data = sr.AudioFile(audio_file)
        with audio_data as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            recognizer.energy_threshold = 300
            recognizer.pause_threshold = 1.0
            audio_content = recognizer.listen(source)

    try:
        texto = recognizer.recognize_google(audio_content, language='es-ES')
    except sr.UnknownValueError:
        texto = "No se pudo entender el audio"
    except sr.RequestError as e:
        texto = f"Error al conectarse con el servicio de Google: {e}"

    return texto



# Función encargada de procesar texto
def procesar_texto(texto):
    texto = texto.lower()  # convierte el texto a minúsculas
    texto = re.sub(r'[,\.;:!\-*#@$!+_%^&`~]', '', texto)  # Elimina los caracteres especiales
    texto = re.sub(r'\s+', ' ', texto)  # Elimina los espacios en blanco adicionales

    thresgold = 1  # se establece el umbral para la longitud mínima de las palabras

    doc = nlp(texto)  # Se pre-procesa el texto utilizando la clase pre-etrenada de spaCy

    # Se obtienen los tokens, lemas y etiquetas de parte del discurso para las palabras filtradas
    tokens = [token.text for token in doc]
    # se definen la lista de palabras que no aportan
    stopwords = spacy.lang.es.stop_words.STOP_WORDS
    # se filtran los tokens por medio de diversas condiciones
    filtered_tokens = [
        token.text for token in doc # se recorre cada token de la entrada
        if token.text not in stopwords # si comprueba que el token este fuera de un stopword
        and token.pos_ in ('NOUN', 'ADJ', 'ADP') # se comprueba que la etiqueta gramatical del token sea sustantivo, adjetivo o proposicion
        and len(token.text) > thresgold # Se comprueba que la longitud del token sea mayor al umbral previamente establecido
        ]
    lemmas = [token.lemma_ for token in doc if token.text in filtered_tokens]
    pos_tags = [(token.text, token.pos_) for token in doc if token.text in filtered_tokens]

    return {
        "tokens": tokens,
        "lemmas": lemmas,
        "filtered_tokens": filtered_tokens,
        "pos_tags": pos_tags,
    }


@router.get("/search-by-text/{userId}", response_class=HTMLResponse)
async def searchByText(request: Request, userId: str):
    return templates.TemplateResponse("search-by-text.html", {"request": request, "userId": userId})


@router.get("/search-by-text/{userId}/texto", response_class=HTMLResponse)
async def searchByText(request: Request, userId: str):
    return templates.TemplateResponse("consulta_texto.html", {"request": request, "userId": userId})

@router.get("/search-by-text/{userId}/audio", response_class=HTMLResponse)
async def searchByText(request: Request, userId: str):
    return templates.TemplateResponse("consulta_voz.html", {"request": request, "userId": userId})

def entrada_voz():
    recognizer = sr.Recognizer()  # Se inicializa el objeto de la clase speech recognition con el metodo recognizer y almacena en la variable 'recognizer'
    mic = sr.Microphone()  # Configuración del micrófono como fuente de audio

    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        # Ajuste de sensibilidad y tiempo de pausa
        recognizer.energy_threshold = 300  # Ajustar según el entorno
        recognizer.pause_threshold = 1.0  # Ajustar según necesidad
        print("Por favor, habla ahora.")  # Indicación para el usuario
        audio = recognizer.listen(source)  # Escucha y captura del audio mientras escuche entrada de voz continua

    try:
        texto = recognizer.recognize_google(audio, language='es-ES')  # Reconocimiento de voz utilizando Google
    except sr.UnknownValueError:
        print("No se pudo entender el audio")  # Manejo de error en caso de audio no reconocido
    except sr.RequestError as e:
        print("Error al conectarse con el servicio de Google: {0}".format(e))  # Manejo de error en la conexión con Google

    return texto  # retorna el texto reconocido por audio



@router.get("/process-texto")
async def process_input(request: Request, texto: str = Query(...)):
    print("in", texto)
    # Defino el diccionario donde se almacenara la informacion de entrada y salida de la consulta
    consulta_dict = {}
    
    # Procesar texto
    texto_analizado = procesar_texto(texto)
    tokens = texto_analizado['tokens']
    tokens_filtrados = texto_analizado['filtered_tokens']
    lemmas_filtrados = texto_analizado['lemmas']
    pos_tags_filtrados = texto_analizado['pos_tags']

    df_frutas_verduras['producto_tokens_lemmas'] = df_frutas_verduras['Producto'].apply(lambda x: procesar_texto(x)['lemmas'])

    dict_count_coincidences = {}

    for index, row in df_frutas_verduras.iterrows():  # Iterar sobre las filas del DataFrame
        for token_producto in row['producto_tokens_lemmas']:  # Iterar sobre los tokens lematizados de la columna 'producto_tokens_lemmas'
            if token_producto in lemmas_filtrados:  # Verificar si el token lematizado está en la lista de lemas filtrados de la entrada del usuario
                if token_producto not in dict_count_coincidences:  # Si el token no está en el diccionario de coincidencias
                    dict_count_coincidences[index] = 1  # Agregar el token al diccionario con el valor 1
                else:  # Si el token ya está en el diccionario de coincidencias
                    dict_count_coincidences[index] += 1  # Incrementar el valor del token en el diccionario

    series_ordered_count_coincidences = pd.Series(dict_count_coincidences)

    consulta_dict['id_consulta'] = None  # ID de la consulta (aún no asignado)
    consulta_dict['id_cliente'] = None  # ID del cliente (aún no asignado)
    # consulta_dict['formato_consulta'] = entrada_tipo  # Formato de la consulta (aún no especificado)
    consulta_dict['entrada_usuario'] = texto  # Transcripción del audio (aún no disponible)
    consulta_dict['entrada_lemas_filtrados'] = lemmas_filtrados  # Lemas filtrados de la entrada del usuario
    consulta_dict['dict_producto_indice_considencias'] = dict_count_coincidences  # Diccionario de productos y sus coincidencias
    consulta_dict['card_recomendacion'] = None  # Tarjeta de recomendación (aún no generada)
    audio_recomendacion = None  # Audio de la recomendación (aún no generado)

    df_frutas_verduras['Precio'] = df_frutas_verduras['Precio'].apply(common_functions.limpiar_signo_peso)
    series_ordered_count_coincidences = series_ordered_count_coincidences.sort_values(ascending=False)

    recomendacion = 'Los productos recomendados basados en su consulta y características mencionadas son:\n'
    lista_string_reco_supers_prods = []

    for count, x in enumerate(series_ordered_count_coincidences.index, start=1):
        producto, supermercado, precio = df_frutas_verduras.loc[x, ['Producto', 'Supermercado', 'Precio']]
        lista_string_reco_supers_prods.append(f'En la posición {count}: {producto} en {supermercado} a {precio} pesos\n')

    recomendacion += ''.join(lista_string_reco_supers_prods)
    recomendacion = common_functions.redondear_numeros(recomendacion)
    consulta_dict['card_recomendacion'] = recomendacion

    tts = gTTS(text=recomendacion, lang='es')
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    consulta_dict['recomendacion_audio'] = audio_buffer

    recomendaciones = consulta_dict['card_recomendacion'].replace("\n", "<br>")

    print("consulta_dict",consulta_dict)

    return templates.TemplateResponse("consulta_texto.html", {"request": request, "recomendaciones": recomendaciones})


@router.get("/process-audio")
async def process_input(request: Request):
    texto = entrada_voz()
    print("in", texto)
    # Defino el diccionario donde se almacenara la informacion de entrada y salida de la consulta
    consulta_dict = {}
    
    # Procesar texto
    texto_analizado = procesar_texto(texto)
    tokens = texto_analizado['tokens']
    tokens_filtrados = texto_analizado['filtered_tokens']
    lemmas_filtrados = texto_analizado['lemmas']
    pos_tags_filtrados = texto_analizado['pos_tags']

    df_frutas_verduras['producto_tokens_lemmas'] = df_frutas_verduras['Producto'].apply(lambda x: procesar_texto(x)['lemmas'])

    dict_count_coincidences = {}

    for index, row in df_frutas_verduras.iterrows():  # Iterar sobre las filas del DataFrame
        for token_producto in row['producto_tokens_lemmas']:  # Iterar sobre los tokens lematizados de la columna 'producto_tokens_lemmas'
            if token_producto in lemmas_filtrados:  # Verificar si el token lematizado está en la lista de lemas filtrados de la entrada del usuario
                if token_producto not in dict_count_coincidences:  # Si el token no está en el diccionario de coincidencias
                    dict_count_coincidences[index] = 1  # Agregar el token al diccionario con el valor 1
                else:  # Si el token ya está en el diccionario de coincidencias
                    dict_count_coincidences[index] += 1  # Incrementar el valor del token en el diccionario

    series_ordered_count_coincidences = pd.Series(dict_count_coincidences)

    consulta_dict['id_consulta'] = None  # ID de la consulta (aún no asignado)
    consulta_dict['id_cliente'] = None  # ID del cliente (aún no asignado)
    # consulta_dict['formato_consulta'] = entrada_tipo  # Formato de la consulta (aún no especificado)
    consulta_dict['entrada_usuario'] = texto  # Transcripción del audio (aún no disponible)
    consulta_dict['entrada_lemas_filtrados'] = lemmas_filtrados  # Lemas filtrados de la entrada del usuario
    consulta_dict['dict_producto_indice_considencias'] = dict_count_coincidences  # Diccionario de productos y sus coincidencias
    consulta_dict['card_recomendacion'] = None  # Tarjeta de recomendación (aún no generada)
    audio_recomendacion = None  # Audio de la recomendación (aún no generado)

    df_frutas_verduras['Precio'] = df_frutas_verduras['Precio'].apply(common_functions.limpiar_signo_peso)
    series_ordered_count_coincidences = series_ordered_count_coincidences.sort_values(ascending=False)

    recomendacion = 'Los productos recomendados basados en su consulta y características mencionadas son:\n'
    lista_string_reco_supers_prods = []

    for count, x in enumerate(series_ordered_count_coincidences.index, start=1):
        producto, supermercado, precio = df_frutas_verduras.loc[x, ['Producto', 'Supermercado', 'Precio']]
        lista_string_reco_supers_prods.append(f'En la posición {count}: {producto} en {supermercado} a {precio} pesos\n')

    recomendacion += ''.join(lista_string_reco_supers_prods)
    recomendacion = common_functions.redondear_numeros(recomendacion)
    consulta_dict['card_recomendacion'] = recomendacion

    tts = gTTS(text=recomendacion, lang='es')
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    consulta_dict['recomendacion_audio'] = audio_buffer

    recomendaciones = consulta_dict['card_recomendacion'].replace("\n", "<br>")

    print("consulta_dict",consulta_dict)

    return templates.TemplateResponse("consulta_voz.html", {"request": request, "recomendaciones": recomendaciones})
