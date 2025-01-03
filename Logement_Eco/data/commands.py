import sqlite3

def get_db(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        return conn
    except sqlite3.Error as e:
        print(f"Erreur de connexion à la base de données: {e}")
        exit(1)

def read_scrpit(file_path: str):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError as e:
        print(f"Erreur lors de la lecture du fichier SQL: {e}")
        exit(1)

def run_script(conn, sql_script: str):
    try:
        conn.executescript(sql_script)
        print("Script exécuté avec succès!")
    except sqlite3.Error as e:
        print(f"Erreur lors de l'exécution du script SQL: {e}")
    finally:
        conn.commit()
        conn.close()

# Lire le fichier SQL
# print("Lecture du Logement.sql")
sql_script = read_scrpit('logement.sql')

# Connexion à la base de données
c = get_db('logement.db')

# Exécuter le script SQL complet
run_script(c, sql_script)

# Lire le fichier SQL
# print("Lecture du insere.sql")
sql_script_insert = read_scrpit('insere.sql')

# Connexion à la base de données
c = get_db('logement.db')

# Exécuter le script SQL complet
run_script(c, sql_script_insert)