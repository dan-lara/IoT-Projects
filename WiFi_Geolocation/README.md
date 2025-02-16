# TP2 - Géolocalisation avec WiFi 

[![View du Projet](https://raw.githubusercontent.com/dan-lara/IoT-Projects/master/LoRaTemp/front.png)](https://iot-projects-tp2.streamlit.app/)

Voici le lien : https://iot-projects-tp2.streamlit.app/

Ce projet a été développé pour surveiller la température à distance en utilisant la technologie LoRa. Mon application permet de :

- Surveiller la température en temps réel
- Visualiser les données des capteurs
- Configurer et gérer les capteurs

## Comment Tester le Projet 🚀

### Prérequis
- [Python 3](https://www.python.org/)
- [SQLite 3](https://www.sqlite.org/)

### Installation
```bash
# Cloner le dépôt
git clone git@github.com:dan-lara/IoT-Projects.git

# Déplacer vers le dossier du Projet
cd WiFi_Geolocation
```
### Démarrage
```bash
# Aller dans le répertoire du serveur
cd srv

# Créer un environnement virtuel
python -m venv .venv

# Installer les dépendances
pip install -r requirements.txt

# Activer l'environnement virtuel
source .venv/bin/activate

# Lancer l'application Streamlit
streamlit run app:main
```
### Arduino
```markdown
1. Connecter le module LoRa à la carte Arduino.
2. Ouvrir le fichier `TP2.ino` dans l'IDE Arduino.
3. Sélectionner le bon port et la bonne carte dans l'IDE Arduino.
4. Télécharger le code sur la carte Arduino.
```

# Architecture du Projet 🏗️

### Structure des Fichiers
```
└── 📁WiFi_Geolocation
    └── 📁src
        └── LoRaModule.cpp
        └── LoRaModule.h
        └── TP2.ino
        └── WiFiSniffer.cpp
        └── WiFiSniffer.h
    └── 📁srv
        └── app.py
        └── 📁data
            └── BDD.csv
            └── geoloc_data.db
        └── exemple.env
        └── gestion_bdd.py
        └── localisateur.py
        └── mqtt_server.py
        └── requirements.txt
        └── trilateration.py
        └── 📁utils
            └── csv_kml_tools.py
            └── ttn.py
    └── front.png
    └── Rapport.pdf
    └── README.md
```

# Comment Contribuer 🤝
1. Forker le projet
2. Créer une branche (`git checkout -b feature/VotreFunctionalite`)
3. Commit vos changements (`git commit -m 'Add some VotreFunctionalite'`)
4. Push vers la branche (`git push origin feature/VotreFunctionalite`)
5. Ouvrir une Pull Request
