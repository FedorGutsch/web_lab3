from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.models.token import RefreshToken
from app.schemas.users import UserCreate
from app.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)

def register(db: Session, data: UserCreate) -> User:
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "Email already registered")
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(400, "Username already taken")
    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login(db: Session, email: str, password: str) -> dict:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")
    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)
    db_token = RefreshToken(
        token=refresh,
        user_id=user.id,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )
    db.add(db_token)
    db.commit()
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}

def refresh(db: Session, token_str: str) -> dict:
    token_record = db.query(RefreshToken).filter(
        RefreshToken.token == token_str,
        RefreshToken.revoked == False
    ).first()
    if not token_record or token_record.expires_at < datetime.utcnow():
        raise HTTPException(401, "Refresh token invalid or expired")
    try:
        payload = decode_token(token_str)
    except Exception:
        raise HTTPException(401, "Invalid refresh token")
    if payload.get("type") != "refresh":
        raise HTTPException(401, "Not a refresh token")
    user_id = int(payload.get("sub"))
    # отзываем старый токен
    token_record.revoked = True
    db.commit()
    # выпускаем новую пару
    new_access = create_access_token(user_id)
    new_refresh = create_refresh_token(user_id)
    db.add(RefreshToken(
        token=new_refresh,
        user_id=user_id,
        expires_at=datetime.utcnow() + timedelta(days=7)
    ))
    db.commit()
    return {"access_token": new_access, "refresh_token": new_refresh, "token_type": "bearer"}

def logout(db: Session, token_str: str):
    token_record = db.query(RefreshToken).filter(RefreshToken.token == token_str).first()
    if token_record:
        token_record.revoked = True
        db.commit()
    return {"detail": "Logged out"}