# Create and activate virtual env for speech processing stage
import re
import spacy
from spacy.training import Example
from spacy.util import minibatch
from spacy import displacy

# Función encargada de procesar texto
def procesar_texto(texto, graph=None, nlp = None):
    texto = texto.lower()  # convierte el texto a minúsculas
    texto = re.sub(r'[,\.;:!\-*#@$!+_%^&`~]', '', texto)  # Elimina los caracteres especiales
    texto = re.sub(r'\s+', ' ', texto)  # Elimina los espacios en blanco adicionales

    thresgold = 1  # se establece el umbral para la longitud mínima de las palabras

    doc = nlp(texto)  # Se pre-procesa el texto utilizando la clase pre-etrenada de spaCy

    if graph == True:
        displacy.render(doc, style='dep', options={'distance':100})

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

def limpiar_signo_peso(texto):
    try:
        texto = texto.replace('$', '')  # Eliminar el símbolo de dólar
        texto = texto.replace('.', '')  # Eliminar los puntos de separación de miles
        texto = texto.replace(',', '.')  # Reemplazar la coma decimal por un punto
        precio = int(float(texto))
    except:
        precio = None
    return precio # Convertir a número flotante y luego a entero

def redondear_numeros(texto):
    # Buscar todos los números con decimales
    numeros = re.findall(r'\d+\.\d+', texto)
    for numero in numeros:
        # Convertir a entero (redondear eliminando decimales)
        entero = str(int(float(numero)))
        # Reemplazar en el texto
        texto = texto.replace(numero, entero)
    return texto