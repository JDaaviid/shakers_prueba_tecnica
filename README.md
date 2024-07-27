# Prueba técnica SHAKERS

Este repositorio contiene la documentación de la prueba técnia desarrollada para SHAKERS.

## Tabla de contenidos
1. [Tecnología usada](#tecnología-usada)
2. [Instrucciones de instalación](#instrucciones-de-instalación)
3. [Estructura del proyecto](#estructura-del-proyecto)
4. [Pruebas realizadas](#pruebas-realizadas)
5. [Documentación de la API](#documentación-de-la-api)


## Tecnología usada

- **FastAPI**:: Un marco web moderno y rápido (de alto rendimiento) para construir APIs con Python.
- **MySQL**: Un sistema de gestión de bases de datos relacional de código abierto.


## Instrucciones de instalación

### prerrequisitos

- Python 3.12
- Varias librerías de Python (incluídas en requirements.txt)
- Base de datos MySQL.



### Pasos

1. **Clonar el respositorio**

    ```sh
    git clone https://github.com/JDaaviid/shakers_prueba_tecnica.git
    cd shakers_prueba_tecnica
    ```
2. **Crear un entorno de Anaconda**

    conda create --name shakers python=3.12


3. **Instalar las dependiencias en el entorno**

    pip install -r requirements.txt

4. **Establecer la base de datos con MySQL en el localhost:3306**
    CREATE USER 'rootShakers'@'localhost' IDENTIFIED BY 'root&Password1';
    GRANT ALL PRIVILEGES ON titanic_db.* TO 'rootShakers'@'localhost';
    FLUSH PRIVILEGES;

5. **Actualizar variables de entorno en .env**

4. **Ejecutar la API en el puerto 8000**

    python main.py

5. **Ejecutar el archivo de pruebas test_main.py**
    python test_main.py


## Estructura del proyecto

La estructura del proyecto es la siguiente:

- **`database.py`**: Configuración para la base de datos.
- **`dataset/`**: Carpeta que contiene los archivos CSV del conjunto de datos.
  - **`gender_submission.csv`**
  - **`test.csv`**
  - **`train.csv`**
- **`main.py`**: Archivo principal para ejecutar la aplicación.
- **`models.py`**: Definición de los modelos de datos.
- **`predict.py`**: Script para realizar predicciones.
- **`requirements.txt`**: Lista de dependencias del proyecto.
- **`test_main.py`**: Pruebas para el archivo principal de la aplicación.
- **`train.py`**: Script para entrenar el modelo.


## Pruebas realizadas
El script de python para realizar varias pruebas es test_main.py

Este código tiene realiza las siguientes pruebas:

Tras ejecutar el script de python que realiza varias pruebas en la API
1. load_passengers() -> Hace una llamada a la API para cargar los pasajeros del dataset del titanic train.csv en la base de datos MySQL.

2. train_model() -> Hace una llamada a la API para entrenar un modeo de clasificación RandomForest. En la llamada se pasa el API_TOKEN para solo permitir procesar la petición a alguien autorizado.

3. test_predict_endpoint() -> Llamada a la API para, tras haber entrenado el modelo con la función anterior, hacer una predicción de si un pasajero con determinadas características sobrevivió o no. En la llamada se utiliza el API_TOKEN.

4. test_predict_invalid_input() -> Llamada a la API para hacer una predicción de un pasajero con valores con tipos no válidos. Concretamente, "Pclass" se pasa como un valor string en lugar de un integer, el cual es el esperado por el modelo. En la llamada se utiliza el API_TOKEN.

5. test_add_passenger() -> Llamada a la API para añadir un pasajero a la base de datos. En la llamada se utiliza el API_TOKEN.


### Resultados de ejecutar test_main.py
$ python test_main.py 

OUTPUT EN CONSOLA:
```
Starting tests...
Response Status Code: 200
Response Body: {"message":"Passengers loaded successfully"}
Model trained with accuracy: 0.7622377622377622
Train Model Response Status Code: 200
Train Model Response Body: {"message":"Training started in background"}
Training completed. Running tests...
Prediction request status code: 200
Prediction request response: {'prediction': [0]}
Invalid input request status code: 422
Invalid input request response: {'detail': [{'type': 'int_parsing', 'loc': ['body', 'Pclass'], 'msg': 'Input should be a valid integer, unable to parse string as an integer', 'input': 'invalid'}]}
Add passenger request status code: 200
Add passenger request response: {'message': 'Passenger added', 'passenger_id': 896}
All tests completed.
```

Adicionalmente, se generan los archivos confusion_matrix.txt, model.pkl y la carpeta mlruns para la observabilidad de los resultados del entrenamiento realizado.


## Documentación de la API

A continuación se detallan los endpoints de la API:

1. **`/load-passengers`** -> Carga los pasajeros en la base de datos.
2. **`/train`** -> Entrena el modelo.
3. **`/predict`** -> Predice si el pasajero ha sobrevivido o no.
4. **`/add_passenger`** -> Añade un nuevo pasajero a la base de datos.





