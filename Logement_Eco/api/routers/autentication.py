from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import APIKeyHeader
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from autentication import (
    create_user, authenticate_user, create_access_token, decode_jwt, create_api_key, validate_api_key, ACCESS_TOKEN_EXPIRE_MINUTES
)
from datetime import timedelta, datetime
from tools import get_db
from sqlite3 import Connection

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Route for user registration
@router.post("/register_user", tags=["Auth"])
def register_user(username: str, password: str):
    try:
        create_user(username, password)
        return {"message": "User created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Route for user login (token generation)
@router.post("/token", tags=["Auth"])
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Dependency to verify JWT
async def verify_jwt(token: str = Depends(oauth2_scheme)):
    username = decode_jwt(token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return username

# Route for API key generation
@router.post("/register_api-key", tags=["Auth"])
def register_api_key(api_key: str, description: Optional[str] = None):
    """Register a new API key for microcontrollers."""
    try:
        create_api_key(api_key, description)
        return {"message": "API key registered successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

async def verify_api_key(api_key: Optional[str] = Depends(APIKeyHeader(name="X-API-Key", auto_error=False))):
    if not api_key or not validate_api_key(api_key):
        raise HTTPException(
            status_code=403, detail="Invalid API Key"
        )
    return api_key


from fastapi import APIRouter, Depends
from models.database import Mesure
@router.post("/api-key", response_model=Mesure, tags=["Mesure"])
def create_mesure(
    mesure: Mesure,
    db: Connection = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    if validate_api_key(api_key):
        query = """
        INSERT INTO Mesure (id_c, valeur, created_at)
        VALUES (?, ?, ?)
        """
        if mesure.created_at is None:
            mesure.created_at = datetime.now()
        cursor = db.execute(query, (mesure.id_c, mesure.valeur, mesure.created_at))
        db.commit()
        mesure_id = cursor.lastrowid
        return {**mesure, "id": mesure_id}
    else:
        raise HTTPException(status_code=403, detail="Invalid API Key")
