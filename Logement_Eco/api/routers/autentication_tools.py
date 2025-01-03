import sqlite3
from datetime import datetime, timedelta
from typing import Optional, List
import jwt  # pyJWT
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
AUTH_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/auth.db"))


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
            user_logements LIST INTEGER,
            user_api_keys LIST INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        # API keys table for microcontrollers
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            key TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()


def create_user(username: str, password: str, user_logements: List[int] = None):
    """Create a new user in the authentication database."""
    hashed_password = pwd_context.hash(password)
    init_auth_db()
    with sqlite3.connect(AUTH_DB_PATH) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, hashed_password, user_logements) VALUES (?, ?, ?)",
                (username, hashed_password, ','.join(map(str, user_logements))),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError("User already exists")
        try:
            cursor.execute(
                "SELECT id FROM users WHERE username = ?", (username,)
            )
            user_id = cursor.fetchone()[0]
            create_api_key(user_id, "Default", "Default API key")
            return user_id
        except sqlite3.Error:
            raise ValueError("User not found")


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

def validate_token(token: str) -> Optional[dict]:
    """Validate a JWT token and return user details."""
    username = decode_jwt(token)
    if username:
        with sqlite3.connect(AUTH_DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_logements, user_api_keys, id FROM users WHERE username = ?", (username,)
            )
            result = cursor.fetchone()
            if result:
                user_logements = result[0].split(',') if result[0] else []
                user_api_keys_ids = str(result[1]).split(',') if result[1] else []
                user_id = result[2]
                user_api_keys = []
                for api_key_id in user_api_keys_ids:
                    cursor.execute(
                        "SELECT name, key FROM api_keys WHERE id = ?", (api_key_id,)
                    )
                    api_key_result = cursor.fetchone()
                    if api_key_result:
                        user_api_keys.append({"name": api_key_result[0], "key": api_key_result[1]})
                return {
                    "username": username,
                    "user_id": user_id,
                    "user_logements": user_logements,
                    "user_api_keys": user_api_keys
                }
    return None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generate a JWT access token."""
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return token


def decode_jwt(token: str) -> Optional[str]:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        print("Token expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None


def create_api_key(user_id: str, name: str, description: str = None):
    """Register a new API key for microcontrollers."""
    api_key = secrets.token_urlsafe(32)
    with sqlite3.connect(AUTH_DB_PATH) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO api_keys (user_id, name, description, key) VALUES (?, ?, ?, ?)",
                (user_id, name, description, api_key),
            )
            conn.commit()
            api_key_id = cursor.lastrowid          
            cursor.execute(
                "SELECT user_api_keys FROM users WHERE id = ?", (user_id,)
            )
            result = cursor.fetchone()
            user_api_keys = result[0] if result else None
            # print(user_api_keys)
            if user_api_keys:
                user_api_keys = str(user_api_keys).split(',')
            else:
                user_api_keys = []
            user_api_keys.append(str(api_key_id))
            cursor.execute(
                "UPDATE users SET user_api_keys = ? WHERE id = ?",
                (','.join(user_api_keys), user_id),
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

#     user_id = create_user("admin", "admin")
#     print("User created: admin")
#     jwt_admin = authenticate_user("admin", "admin")
#     jwt_invalid = authenticate_user("admin", "wrong")
#     print("JWT token for admin:", jwt_admin)
#     print("JWT token for invalid credentials:", jwt_invalid)
#     print("Decoding JWT token:", decode_jwt(jwt_admin))
#     print("Decoding invalid JWT token:", decode_jwt(jwt_invalid))

#     print("-" * 20)
#     print("API key creation and validation")
#     key = create_api_key(user_id, "ESP32", "First microcontroller")
#     key = create_api_key(user_id, "Second", "Second microcontroller")
#     print(f"API key created: {key}")
#     print("Validating key:", validate_api_key(key))
