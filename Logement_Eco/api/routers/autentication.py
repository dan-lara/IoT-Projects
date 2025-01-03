from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from typing import Optional, List
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .autentication_tools import (
    create_user, authenticate_user, create_access_token, decode_jwt, create_api_key, validate_api_key, ACCESS_TOKEN_EXPIRE_MINUTES, validate_token
)
from datetime import timedelta, datetime
from ..tools import get_db
from sqlite3 import Connection


# Configuration pour la clé API
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def get_api_key(api_key: str = Security(api_key_header)):
    """Vérifie la clé API."""
    if not validate_api_key(api_key):
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

router = APIRouter()

# Route pour générer une nouvelle clé API
@router.post("/api_key", tags=["Auth"])
def generate_api_key(token: str, name: str, description: str = None):
    user_data = decode_token(token)
    api_key = create_api_key(user_data["user_id"], name, description)
    return {"api_key": api_key, "description": description, "username": user_data["username"]}

# Route pour authentifier un utilisateur
@router.post("/login", tags=["Auth"])
def login(username: str, password: str):
    token = authenticate_user(username, password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}

# Route pour décoder un JWT
@router.post("/decode", tags=["Auth"])
def decode_token(token: str):
    user_data = validate_token(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user_data

@router.post("/register_user", tags=["Auth"])
def register_user(username: str, password: str, user_logements: List[int] = None):
    try:
        create_user(username, password, user_logements)
        return {"message": "User created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
