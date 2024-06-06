# Asistente inteligente

![portada](./datos/procesaodos/portada.png)

## Estado del Proyecto
- **En proceso**

## Estructura de Directorios y Archivos Resultantes


    Asistente inteligente
    │
    ├── DatosPreciosSupermercado # CSV's
    | |
    │ ├── procesados # .csv procesados
    │ └── limpios # .csv en bruto
    │
    ├── notebooks # Cuadernos y guiones
    |   |
    │   |-- 1_comprensión_datos.ipynb
    |   |__ 2_preparacion_datos.ipynb
    |   |__ 2_preparacion_datos.ipynb
    |   |__ 3_modelado.ipynb
    |   |__ 4_evaluación.ipynb
    |   |__ 5_despliegue.ipynb
    │
    ├── .gitignore
    │
    ├── REQUIREMENTS.txt
    |
    │-- LICENSE.md
    │
    └── README.md 


## Funciones y Aplicaciones
- Entender las necesidades del usuario a través de comandos de voz
- Buscar productos que se adapten a estas necesidades
- Comparar precios en diferentes tiendas en línea para sugerir la mejor opción.
- Seguimiento de los pedidos
- Realizar el seguimiento de los pedidos y notificar al usuario sobre la entrega

### Explicacion
- 

## Tecnologías Utilizadas
- **Programing language:**
  - **Python**
    - *Libreiras para analisis de datos*
      - *numpy*
      - *pandas*
      - *missingno*

    - *Librerias para visualizacion de datos:*
      - *matplotlib*
      - *seaborn*
      - *folium*

    - *Librerias para aprendizaje automatico:*
      - *scikit-learn*
      - *joblib*

    - *Librerias para aprendizaje profundo:*
      - *NLP*
        - *NLTK*

## Instalación de Paquetes
```bash
pip3 install -r requerimientos.txt
```

## Despliegue de la Aplicación en local 

- Descargar el repositorio  [2024_asistente_compras](https://github.com/ianCristianAriel/2024_asistente_compras) o clonarlo 
```bash
git clone https://github.com/ianCristianAriel/2024_asistente_compras.git
```

- Acceder al repositorio clonado
```bash
cd 2024_asistente_compras
```

- Intalar dependencias necesarias
```bash
pip install fastapi 
```
```bash
pip install uvicorn
```
```bash
pip install jinja2 
```
```bash
pip install pandas
```
```bash
pip install tensorflow
```
```bash
pip install speechrecognition
```
```bash
pip install spacy
```
```bash
pip install nltk
```
```bash
pip install gtts
```
```bash
pip install pydub
```

```bash
pip install pillow
```

- Descargar el modelo es_core_news_sm
```bash
python -m spacy download es_core_news_sm
```

- Acceder a la carpeta notebooks y scripts
```bash
cd '.\notebooks y scripts\'
```

- Acceder a la carpeta cd 5_despliegue
```bash
cd .\5_despliegue\
```

- Desplegar la aplicación web 
```bash
uvicorn app.main:app --reload
```

- Ingresar a la aplicación 

    - Colocar en el navegador la dirección [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

- Navegar en la aplicación


## Personas Desarrolladoras del Proyecto:

- [goncor](https://github.com/GonCor)
- [tomasescobar25](https://github.com/tomasescobar25)
- [agustinar](https://github.com/agustinarr)
- [IanCristianAriel](https://github.com/ianCristianAriel)
- [ClaudineMeyer](https://github.com/ClaudineMeyer)
- [Francisco-B07](https://github.com/Francisco-B07)