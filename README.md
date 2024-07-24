# FastAPI Project

## Description

Ce projet utilise [FastAPI](https://fastapi.tiangolo.com/) pour créer une API rapide et efficace. Il utilise également Alembic pour la gestion des migrations de base de données.

## Prérequis

Assurez-vous d'avoir les éléments suivants installés sur votre machine :

- Python 3.12
- `pip` (gestionnaire de paquets Python)

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/Alexis3386/food-for-dev-api.git
cd food-for-dev-api
```

### 2. Créer et activer un environnement virtuel

```bash
python -m venv .venv
source .venv/bin/activate    # Pour Linux/Mac
.venv\Scripts\activate       # Pour Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Créer un fichier .env

À la racine du projet, créez un fichier .env et ajoutez-y les informations suivantes

DATABASE_URL=sqlite:///./test.db  # Remplacez par l'URL de votre base de données
SECRET_KEY=your_secret_key       # Remplacez par votre clé secrète

### 5. Initialiser Alembic
```bash
alembic init alembic
```

### 6. Exécuter les migrations
Appliquez les migrations pour configurer la base de données :

```bash
alembic upgrade head
```
## Démarrage du serveur
Pour démarrer le serveur FastAPI, deplacer vous dans le dosiier src et exécutez :
```bash
uvicorn main:app --reload
```

Le serveur sera disponible à l'adresse http://127.0.0.1:8000.

## Documentation de l'API
Une fois le serveur en cours d'exécution, vous pouvez accéder à la documentation interactive de l'API à l'adresse http://127.0.0.1:8000/docs.