# Prueba técnica SHAKERS

Este repositorio contiene la documentación de la prueba técnia desarrollada para SHAKERS.

## Tabla de contenidos
1. [Tecnología usada](#technology-used)
2. [Instrucciones de instalación](#install-instructions)
3. [Otra información relevante](#other-relevant-info)
4. [Documentación de la API](#api-documentation)


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

├── database.py
├── dataset
│   ├── gender_submission.csv
│   ├── test.csv
│   └── train.csv
├── main.py
├── models.py
├── predict.py
├── requirements.txt
├── test_main.py
└── train.py

## Pruebas realizadas
El script de python para realizar varias pruebas es test_main.py

Este código tiene las siguientes funciones



### Resultados de ejecutar test_main.py
Tras ejecutar el script de python que realiza varias pruebas en la API


