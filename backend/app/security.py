# app/security.py
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.config import settings

ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = 15
REFRESH_TOKEN_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_token(data: dict, expires_delta: timedelta, token_type: str) -> str:
    to_encode = data.copy()
    now = datetime.utcnow()
    to_encode.update({"iat": now, "exp": now + expires_delta, "type": token_type})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

def create_access_token(user_id: int) -> str:
    return create_token({"sub": str(user_id)}, timedelta(minutes=ACCESS_TOKEN_MINUTES), "access")

def create_refresh_token(user_id: int) -> str:
    return create_token({"sub": str(user_id)}, timedelta(days=REFRESH_TOKEN_DAYS), "refresh")

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])