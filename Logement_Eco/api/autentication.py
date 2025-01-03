import sqlite3
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
import secrets

# Load environment variables from .env file
load_dotenv()

# Constants for JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE", 15))

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# SQLite database connection
AUTH_DB_PATH = "../data/auth.db"


def init_auth_db():
    """Initialize the authentication database."""
    with sqlite3.connect(AUTH_DB_PATH) as conn:
        cursor = conn.cursor()
        # Users table for front-end applications
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        # API keys table for microcontrollers
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            key TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()


def create_user(username: str, password: str):
    """Create a new user in the authentication database."""
    hashed_password = pwd_context.hash(password)
    with sqlite3.connect(AUTH_DB_PATH) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, hashed_password) VALUES (?, ?)",
                (username, hashed_password),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError("User already exists")


def authenticate_user(username: str, password: str) -> Optional[str]:
    """Authenticate a user by checking their credentials."""
    with sqlite3.connect(AUTH_DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT hashed_password FROM users WHERE username = ?", (username,)
        )
        result = cursor.fetchone()
        if result and pwd_context.verify(password, result[0]):
            return create_access_token({"sub": username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generate a JWT access token."""
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_jwt(token: str) -> Optional[str]:
    """Decode and validate a JWT token."""
    try:
        if not token:
            raise JWTError("No token provided")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


def create_api_key(name: str, description: str = None):
    """Register a new API key for microcontrollers."""
    api_key = secrets.token_urlsafe(32)
    with sqlite3.connect(AUTH_DB_PATH) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO api_keys (name, description, key) VALUES (?, ?, ?)",
                (name, description, api_key),
            )
            conn.commit()
            return api_key
        except sqlite3.IntegrityError:
            raise ValueError("API key already exists")


def validate_api_key(api_key: str) -> bool:
    """Validate a microcontroller's API key."""
    with sqlite3.connect(AUTH_DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT key FROM api_keys WHERE key = ?", (api_key,)
        )
        result = cursor.fetchone()
        return result is not None


# if __name__ == "__main__":
#     init_auth_db()
#     print("Authentication database initialized")

#     create_user("admin", "admin")
#     print("User created: admin")
#     jwt_admin = authenticate_user("admin", "admin")
#     jwt_invalid = authenticate_user("admin", "wrong")
#     print("JWT token for admin:", jwt_admin)
#     print("JWT token for invalid credentials:", jwt_invalid)
#     print("Decoding JWT token:", decode_jwt(jwt_admin))
#     print("Decoding invalid JWT token:", decode_jwt(jwt_invalid))

#     print("-" * 20)
#     print("API key creation and validation")
#     key = create_api_key("ESP32", "First microcontroller")
#     print(f"API key created: {key}")
#     print("Validating key:", validate_api_key(key))


    