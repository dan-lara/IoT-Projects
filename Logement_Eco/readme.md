# Projet de Logement Éco-responsable IoT 🏠
1. [Aperçu du Projet 📱](#aperçu-du-projet-📱)
2. [Architecture du Projet 🏗️](#architecture-du-projet-🏗️)
3. [Fonctionnalités Détaillées 📋](#fonctionnalités-détaillées-📋)
4. [Comment Contribuer 🤝](#comment-contribuer-🤝)
5. [Description Ostensible Complète (DOC) 📜](#description-ostensible-complète)

# Présentation du Projet
![Logo du Projet](https://raw.githubusercontent.com/dan-lara/IoT-Projects/master/Logement_Eco/front/static/imgs/logo.jpeg)

Ce projet a été développé dans le cadre du TP IoT EISE4, visant à créer une solution complète de monitoring et gestion éco-responsable pour les logements. Mon application permet de :

- Surveiller la consommation énergétique en temps réel
- Visualiser les données des capteurs environnementaux
- Suivre les économies réalisées
- Configurer et gérer les différents capteurs/actionneurs

## Comment Tester le Projet 🚀

### Prérequis
- [Docker](https://www.docker.com/)
- [Python 3](https://www.python.org/)
- [SQLite 3](https://www.sqlite.org/)

### Installation
```bash
# Cloner le dépôt
git clone [votre-repo]

# Déplacer vers le dossier du Projet
cd Logement_Eco
```
### Démarrage
```bash
# Déjà sur le dossier du Projet
docker-compose up --build

#Ouvrir http://localhost:3000 dans votre navigateur
#Il y a 2 users default:
#   username: Admin     password: admin
#   username: Daniel    password: daniel
```

# Architecture du Projet 🏗️

### Structure des Fichiers
```
└── 📁Logement_Eco
    └── 📁api
        └── 📁models
        └── 📁routers
        └── 📁static
            └── 📁css
        └── 📁templates
    └── 📁data
    └── 📁firmware
    └── 📁front       
        └── 📁models
        └── 📁routers
        └── 📁static
            └── 📁css
            └── 📁imgs
            └── 📁js
        └── 📁templates
    └── docker-compose.yml
    └── Dockerfile
    └── readme.md
    └── requirements.txt
```
### Modules Principaux du Projet

Le projet est divisé en 4 modules principaux :

- **Api** : Backend et Frontend de l'exercice 2.
- **Data** : Gestion de la base de données, contient tous les fichiers de la base de données ainsi que les fichiers d'insertion des données de base.
- **Front** : Projet pour le frontend final avec l'ensemble du site web et de nombreux fichiers.
- **Firmware** : Projet pour intégrer les capteurs dans le système et prendre des mesures, avec la gestion des clés API.


### Technologies Utilisées
- **Backend**: [Python](https://www.python.org/), [FastAPI](https://fastapi.tiangolo.com/)
- **Frontend**: [Python](https://www.python.org/), [FastAPI](https://fastapi.tiangolo.com/), [HTML5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5), [CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS3), [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- **Base de données**: [SQLite3](https://www.sqlite.org/)

# Fonctionnalités Détaillées 📋

### 1. Monitoring Énergétique
[Description détaillée]

### 2. Gestion des Capteurs
[Description détaillée]

### 3. Analyse des Données
[Description détaillée]

### 4. Interface Utilisateur
[Description détaillée]

## Problèmes Résolus et Défis 💪
- [Liste des défis techniques rencontrés]
- [Solutions implémentées]

# Comment Contribuer 🤝
1. Forker le projet
2. Créer une branche (`git checkout -b feature/VotreFunctionalite`)
3. Commit vos changements (`git commit -m 'Add some VotreFunctionalite'`)
4. Push vers la branche (`git push origin feature/VotreFunctionalite`)
5. Ouvrir une Pull Request

---
---
---
# Description Ostensible Complète

## 1. Module API (`/api`)
Ce module gère toute la couche backend et l'API REST du projet.
```
└── 📁api
        ── api_back.py
        └── api_front.py
        └── autentication.py
        └── 📁models
            └── database.py
            └── meteo.py
        └── 📁routers
            └── autentication_tools.py
            └── autentication.py
            └── 📁bdd
                └── adresse.py
                └── capteur.py
                └── facture.py
                └── generic.py
                └── logement.py
                └── mesure.py
                └── piece.py
                └── type_capteur.py
                └── type_facture.py
                └── ville.py
            └── facture.py
            └── meteo.py
        └── 📁static
            └── 📁css
                └── meteo_style.css
                └── style.css
        └── 📁templates
            └── facture.html
            └── home.html
            └── meteo_form.html
        └── tools.py
```

#### Composants Principaux :
- **api_back.py** : Serveur principal et point d'entrée de l'API
- **api_front.py** : Gestion des routes pour l'interface utilisateur
- **authentication.py** : Gestion de l'authentification

#### Sous-modules :
- **📁models** : Définition des modèles de données avec **pydantic**
- **📁routers** : Gestion des routes API
  - Rotas de BDD: Metodos Post, Getall, Get, pUT e delete para cada tabela
  - 
- **📁bdd** : Gestionnaires de base de données spécifiques

## 2. Module Data (`/data`)
Responsable de la gestion des données et de la structure de la base de données.
```
└── 📁data
    └── auth.db
    └── auth.sql
    └── commands.py
    └── insert_users.py
    └── insere.sql
    └── logement.db
    └── logement.sql
    └── postgres.sql
    └── schema.png
```

#### Fichiers Clés :
- **logement.db** : Base de données principale SQLite
- **auth.db** : Base de données d'authentification
- **logement.sql** : Schéma de la base de données
- **insere.sql** : Scripts d'insertion des données initiales
- **schema.png** : Visualisation du schéma de la base de données

### 3. Module Frontend (`/front`)
Interface utilisateur complète du projet.

```
└── 📁front
        └── api.py
        └── 📁models
            └── bff_models.py
        └── 📁routers
            └── bff.py
            └── pages.py
            └── tools.py
        └── 📁static
            └── 📁css
                └── old_style.css
                └── styles.css
                └── theme.css
            └── 📁imgs
                └── favicon.ico
                └── logo.jpeg
            └── 📁js
                └── dark-mode.js
                └── main.js
        └── 📁templates
            └── accueil.html
            └── configuration.html
            └── dashboard.html
            └── economies.html
            └── index.html
            └── logements.html
            └── login.html
        └── tools.py
```

#### Structure :
- **📁static** : Ressources statiques (CSS, JS, images)
- **📁templates** : Templates HTML
- **api.py** : Interface avec l'API backend
- **tools.py** : Utilitaires frontend

#### Pages Principales :
- accueil.html
- configuration.html
- dashboard.html
- economies.html
- logements.html

### 4. Module Firmware (`/firmware`)
Gestion des capteurs et des mesures physiques.

```
└── 📁firmware
    └── API_Manager.cpp
    └── API_Manager.h
    └── DHT_Manager.cpp
    └── DHT_Manager.h
    └── firmware.ino
```

#### Composants :
- **API_Manager** : Gestion des communications API
- **DHT_Manager** : Gestion des capteurs DHT
- **firmware.ino** : Programme principal Arduino


## Configuration et Déploiement

### Variables d'Environnement
Le projet utilise un fichier `.env` pour la configuration :
- Copier `.example.env` vers `.env`
- Configurer les variables nécessaires

### Docker
Le projet peut être déployé via Docker :
```bash
docker-compose up --build
```

## Dépendances

Les dépendances sont listées dans `requirements.txt`. Installation :
```bash
pip install -r requirements.txt
```

## Architecture Technique

### Base de Données
- SQLite avec python

### API
- FastAPI pour le backend
- Avec authentification JWT et api_key
- Documentation OpenAPI disponible

### Frontend
- HTML5/CSS3/JavaScript
- Support des thèmes clair/sombre
- Interface responsive
- Documentation OpenAPI disponible

### Firmware
- Compatible Arduino
- Support des capteurs DHT
- Communication API REST