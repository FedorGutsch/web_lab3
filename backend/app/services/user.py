from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.schemas.users import UserUpdate

def get_me(current_user: User) -> User:
    return current_user

def update_me(db: Session, current_user: User, updates: UserUpdate) -> User:
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user

def get_user_by_id(db: Session, user_id: int) -> User:
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user

def search_users(db: Session, query: str, limit: int = 20) -> dict:
    q = f"%{query}%"
    users = db.query(User).filter(
        User.username.ilike(q) | User.email.ilike(q)
    ).limit(limit).all()
    total = db.query(User).filter(
        User.username.ilike(q) | User.email.ilike(q)
    ).count()
    return {"users": users, "total": total}