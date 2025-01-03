import sqlite3
from contextlib import contextmanager
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
