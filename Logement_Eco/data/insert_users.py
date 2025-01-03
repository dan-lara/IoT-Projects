import os
import sys

# Ajoute le chemin absolu du répertoire 'api' à sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.routers.autentication_tools import create_user

# Création d'utilisateur
try:
    create_user("Admin", "admin", [i for i in range(1, 8)])
except:
    print("Utilisateur déjà créé")
try:
    create_user("Daniel", "daniel", [3, 4, 5, 6])
except:
    print("Utilisateur déjà créé")