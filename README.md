# Asistente inteligente

![portada](./datos/procesaodos/portada.png)

## Estado del Proyecto
- **En proceso**

## Estructura de Directorios y Archivos Resultantes


    Asistente inteligente
    │
    ├── DatosPreciosSupermercado # CSV's
    | |
    │ ├── procesados # datos procesados
    │ └── brutos # datos de entrada en bruto
    │
    ├── notebooks # Cuadernos y guiones
    |   |
    │   |-- 1_comprension_preparacion_datos
    |   |__ 2_a_modelado_evaluacion_proc_imagenes
    |   |__ 2_b_modelado_evaluacion_proc_habla
    |   |__ 2_c_modelo_recomendacion
    |   |__ 3_despliegue
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

    - *Librerias para aprendizaje automatico:*
      - *scikit-learn*

    - *Librerias para PLN:*
      - *Keras*
      - *spaCy*

    - *Librerias para captura y transcripcion de voz:*
      - Speech Recognition

    - *Librerias para transformar texto a audio:*
      - gTTS

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
pip install -r requirements.txt
```

- Descargar los modelos
```bash
python -m spacy download es_core_news_sm
python -m nltk.downloader wordnet
```

- Acceder a la carpeta notebooks y scripts
```bash
cd '.\notebooks y scripts\'
```

- Acceder a la carpeta 5_despliegue
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