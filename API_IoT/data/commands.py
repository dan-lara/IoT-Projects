import sqlite3

DEBUG = False

def get_db(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        return conn
    except sqlite3.Error as e:
        print(f"Erreur de connexion à la base de données: {e}")
        exit(1)


# Connexion à la base de données
c = get_db('biblio.db')

# Lire le fichier SQL
with open("raw.sql", "r", encoding="utf-8") as file:
    sql_script = file.read()

# Exécuter le script SQL complet
try:
    c.executescript(sql_script)
    print("Script exécuté avec succès!")
except sqlite3.Error as e:
    print(f"Erreur lors de l'exécution du script SQL: {e}")
finally:
    if DEBUG:
        c.execute('SELECT * FROM Etudiant')

        # parcourt ligne a ligne
        r = c.execute('SELECT * FROM Etudiant')
        for raw in r:
            print (raw.keys())
            print(f"[{raw['id']}, {raw['Nom']}, {raw['Prenom']}, {raw['idAd']}]")

    c.close()