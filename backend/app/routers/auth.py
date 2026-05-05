from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.users import UserCreate, UserLogin, UserResponse
from app.schemas.auth import TokenResponse, RefreshRequest, LogoutRequest
from app.database.session import get_db
from app.services import auth as auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    return auth_service.register(db, data)

@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    return auth_service.login(db, data.email, data.password)

@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshRequest, db: Session = Depends(get_db)):
    return auth_service.refresh(db, data.refresh_token)

@router.post("/logout")
def logout(data: LogoutRequest, db: Session = Depends(get_db)):
    return auth_service.logout(db, data.refresh_token)