import re

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