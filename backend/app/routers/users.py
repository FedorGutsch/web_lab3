from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.users import UserResponse, UserUpdate, UserSearchResponse
from app.dependencies import get_current_user
from app.models.user import User
from app.database.session import get_db
from app.services import user as user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
def read_me(current_user: User = Depends(get_current_user)):
    return user_service.get_me(current_user)

@router.put("/me", response_model=UserResponse)
def update_me(updates: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return user_service.update_me(db, current_user, updates)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_by_id(db, user_id)

@router.get("/search", response_model=UserSearchResponse)
def search(query: str = Query(min_length=1), db: Session = Depends(get_db)):
    return user_service.search_users(db, query)