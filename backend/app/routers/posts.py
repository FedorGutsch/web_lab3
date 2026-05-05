from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.posts import PostCreate, PostUpdate, PostResponse, PostFeedResponse
from app.dependencies import get_current_user
from app.models.user import User
from app.database.session import get_db
from app.services import post as post_service

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=PostResponse, status_code=201)
def create_post(data: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return post_service.create_post(db, current_user, data)

@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, data: PostUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return post_service.update_post(db, post_id, current_user, data)

@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post_service.delete_post(db, post_id, current_user)
    return

@router.get("/feed", response_model=PostFeedResponse)
def feed(page: int = 1, size: int = 20, db: Session = Depends(get_db)):
    return post_service.get_feed(db, page, size)

@router.get("/my", response_model=PostFeedResponse)
def my_posts(page: int = 1, size: int = 20, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return post_service.get_my_posts(db, current_user, page, size)

@router.get("/subscriptions", response_model=PostFeedResponse)
def subscription_feed(page: int = 1, size: int = 20, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return post_service.get_subscription_feed(db, current_user, page, size)

@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    return post_service.get_post(db, post_id)