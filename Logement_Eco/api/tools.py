import sqlite3
db_path = "../data/logement.db"
def get_db():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()