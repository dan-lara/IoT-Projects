# API_IoT

## Description
Ce projet est une API pour la gestion des étudiants et des livres dans une bibliothèque. Il utilise FastAPI pour créer les routes et gérer les requêtes.

## Prérequis
- Python 3.8 ou supérieur
- `pip` pour installer les dépendances

## Installation

### Linux

1. Clonez le dépôt:
    ```sh
    git clone https://github.com/dan-lara/IoT-Projects.git
    cd API_IoT
    ```

2. Créez un environnement virtuel et activez-le:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Installez les dépendances:
    ```sh
    pip install -r requirements.txt
    ```

### Windows

1. Clonez le dépôt:
    ```sh
    git clone https://github.com/dan-lara/IoT-Projects.git
    cd API_IoT
    ```

2. Créez un environnement virtuel et activez-le:
    ```sh
    python -m venv venv
    .\venv\Scripts\activate
    ```

3. Installez les dépendances:
    ```sh
    pip install -r requirements.txt
    ```

## Exécution de l'API

### Linux et Windows

1. Assurez-vous que l'environnement virtuel est activé.
2. Lancez l'application FastAPI:
    ```sh
    uvicorn main:app --reload
    ```

3. L'API sera disponible à l'adresse `http://127.0.0.1:8000`.

## Documentation

La documentation interactive de l'API est disponible à l'adresse `http://127.0.0.1:8000/docs#` une fois l'API démarrée.
