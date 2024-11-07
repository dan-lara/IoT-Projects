import sqlite3

def get_db(db_path: str = "biblio.db"):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()