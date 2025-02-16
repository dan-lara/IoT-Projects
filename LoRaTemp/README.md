# TP3 - Surveillance de Température avec LoRa 🌡️

[![View du Projet](https://raw.githubusercontent.com/dan-lara/IoT-Projects/master/LoRaTemp/front.png)](https://tp3-iot-sorbonne.streamlit.app/)

Voici le lien : https://tp3-iot-sorbonne.streamlit.app/


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
cd LoRaTemp
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
1. Connecter le capteur DHT à la carte Arduino.
2. Connecter le module LoRa à la carte Arduino.
3. Ouvrir le fichier `TP3.ino` dans l'IDE Arduino.
4. Sélectionner le bon port et la bonne carte dans l'IDE Arduino.
5. Télécharger le code sur la carte Arduino.
6. Ouvrir le moniteur série pour vérifier les lectures de température et d'humidité.
```


# Architecture du Projet 🏗️

### Structure des Fichiers
```
└── 📁LoRaTemp
    └── 📁srv
        └── .gitignore
        └── app.py
        └── 📁data
            └── temp_hum.db
        └── example.env
        └── gestion_bdd.py
        └── mqtt_server.py
        └── requirements.txt
    └── 📁TP3
        └── DHT_Manager.cpp
        └── DHT_Manager.h
        └── LoRaModule.cpp
        └── LoRaModule.h
        └── TP3.ino
    └── front.png
    └── README.md
```

# Comment Contribuer 🤝
1. Forker le projet
2. Créer une branche (`git checkout -b feature/VotreFunctionalite`)
3. Commit vos changements (`git commit -m 'Add some VotreFunctionalite'`)
4. Push vers la branche (`git push origin feature/VotreFunctionalite`)
5. Ouvrir une Pull Request