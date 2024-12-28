import sqlite3
from typing import Generator
import os

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/logement.db"))

def get_db() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        return conn
    finally:
        conn.commit()

# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import sessionmaker
# DATABASE_URL = f"sqlite:///{db_path}"
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def get_db_alchemy():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# with get_db() as db_conn:
#     r = db_conn.execute("SELECT * FROM Ville")
#     print([
#             {"Code": row["Code"], "Nom": row["Nom"]}
#             for row in r.fetchall()
#         ])
#     print("ok")