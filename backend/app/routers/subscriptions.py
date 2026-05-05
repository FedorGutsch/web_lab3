from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_current_user
from app.models.user import User
from app.database.session import get_db
from app.schemas.subscriptions import SubscriptionResponse, SubscriberList
from app.services import subscription as sub_service

router = APIRouter(tags=["subscriptions"])

@router.post("/subscriptions/{user_id}", response_model=SubscriptionResponse, status_code=201)
def follow(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return sub_service.subscribe(db, current_user, user_id)

@router.delete("/subscriptions/{user_id}", status_code=204)
def unfollow(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sub_service.unsubscribe(db, current_user, user_id)
    return

@router.get("/users/{user_id}/followers", response_model=SubscriberList)
def followers(user_id: int, db: Session = Depends(get_db)):
    return sub_service.get_followers(db, user_id)

@router.get("/users/{user_id}/following", response_model=SubscriberList)
def following(user_id: int, db: Session = Depends(get_db)):
    return sub_service.get_following(db, user_id)