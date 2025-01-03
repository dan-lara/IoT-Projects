# Projet de Logement Éco-responsable IoT 🏠
1. [Aperçu du Projet 📱](#aperçu-du-projet-📱)
2. [Architecture du Projet 🏗️](#architecture-du-projet-🏗️)
3. [Fonctionnalités Détaillées 📋](#fonctionnalités-détaillées-📋)
4. [Comment Contribuer 🤝](#comment-contribuer-🤝)
5. [Description Ostensible Complète (DOC) 📜](#description-ostensible-complète)

# Présentation du Projet
![View du Projet](https://raw.githubusercontent.com/dan-lara/IoT-Projects/master/Logement_Eco/front.png)

Ce projet a été développé dans le cadre du TP IoT EISE4, visant à créer une solution complète de monitoring et gestion éco-responsable pour les logements. Mon application permet de :

- Surveiller la consommation énergétique en temps réel
- Visualiser les données des capteurs environnementaux
- Suivre les économies réalisées
- Configurer et gérer les différents capteurs/actionneurs
- Voir les logements qui m'appartiennent
- Voir les clés api du microcontrôleur à utiliser
- Connecter l'utilisateur avec contrôle de la session (JWT)

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
### Diagramme
![Diagramme](https://raw.githubusercontent.com/dan-lara/IoT-Projects/master/Logement_Eco/diagram.png)


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

### 1. Accueil
Sur la page d'accueil, les utilisateurs peuvent visualiser les macros pour le logement sélectionné et passer aux autres pages.

### 2. Dashboard
Sur le tableau de bord, vous pouvez visualiser les capteurs, les activer et les désactiver individuellement et sélectionner un capteur pour afficher un graphique dynamique de ses mesures.

### 3. Économies
Page permettant d'afficher des graphiques à barres de chaque type de facture au fil du temps, ainsi que le montant total payé et le nombre de factures, et enfin une visualisation des proportions des types de comptes dans le coût total.

### 4. Logement
Sur cette page, nous pouvons voir les macros pour chaque logement d'utilisateur et les sélectionner individuellement pour voir les données sur les autres pages.

### 5. Configuration
Dans les paramètres, nous pouvons voir les clés api, les copier, en créer de nouvelles, les supprimer et nous déconnecter.

## Problèmes Résolus et Défis 💪
Les principaux problèmes rencontrés sont liés aux technologies choisies, l'utilisation de sqlite3 pour faire les requêtes s'est avérée mauvaise, car un moteur avec sqlalchemy serait plus efficace. 

En raison de mon choix initial de Backend, je n'ai pas pu migrer le projet front-end vers le mode react first et j'ai réalisé qu'il serait beaucoup plus rapide avec cette technologie, en raison de sa resuabilité et de la large gamme de bibliothèques qui accéléreraient le travail.

Dans tous les cas, en utilisant jinja et fastapi, il a été possible de construire une solution fonctionnelle et générique avec l'utilisation de cookies, d'authentification et d'api_keys d'une manière intéressante en pensant que tout était implémenté et que les connexions étaient faites à la main.

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
  - Il contient toutes les routes pour les requêtes à la banque, ainsi que l'authentification. Il est très pratique et contient toutes les routes possibles ainsi que des roues génériques.
- **api_front.py** : Gestion des routes pour l'interface utilisateur
  - Routes comme déjà expliquées pour les tests initiaux utilisant l'api externe pour la météorologie
- **authentication.py** : Gestion de l'authentification

#### Sous-modules :
- **📁models** : Définition des modèles de données avec **pydantic**
- **📁routers** : Gestion des routes API
  - Routes BDD : méthodes Post, Getall, Get, Put et delete pour chaque table
  - Routes Facture et Meteo : Définir le front-end initial réalisé dans les premières séances comme proposé dans le projet.

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
- **schema.png** : Visualisation du schéma de la base de données du Logement

Logement

![Diagramme](https://raw.githubusercontent.com/dan-lara/IoT-Projects/master/Logement_Eco/data/logement.png)


Auth

![Diagramme](https://raw.githubusercontent.com/dan-lara/IoT-Projects/master/Logement_Eco/data/auth.png)

## 3. Module Frontend (`/front`)
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
  - Le modèle d'index gère le thème, certains cookies et la barre de navigation, ainsi que le mode sombre, qui est importé dans tous les autres modèles afin que les pages restent standardisées.
  - Chacun des autres chemins est lié à un autre chemin sur le site.
- **api.py** : Interface avec l'API pour le Front et Back-For-Frony
- **tools.py** : Utilitaires universels
- **📁routers** : Fichiers qui configurent tous les routes et plus
  - **Pages.py** : Fichier qui organise la prise en charge des fonctions bff pour placer les données dans le modèle et renvoyer la page HTML.
  - **bff.py** : Fichier étendu complet de toutes les fonctions pertinentes pour communiquer avec le backend via des appels d'api, la validation et le formatage des données, de nouvelles requêtes spéciales pour la visualisation des données. Il est également accessible via l'API pour le débogage de la démo.

#### Pages Principales :
- accueil.html
- configuration.html
- dashboard.html
- economies.html
- logements.html

## 4. Module Firmware (`/firmware`)
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
- HTML5/CSS3/JavaScript/Bootstrap
- Support des thèmes clair/sombre
- Interface responsive avec bootstrap
- Documentation OpenAPI disponible

### Firmware
- Compatible Arduino
- Support des capteurs DHT
- Communication API REST