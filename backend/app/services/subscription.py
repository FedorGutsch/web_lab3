from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.models.subscription import Subscription

def subscribe(db: Session, follower: User, following_id: int) -> Subscription:
    if follower.id == following_id:
        raise HTTPException(400, "Cannot follow yourself")
    following = db.query(User).get(following_id)
    if not following:
        raise HTTPException(404, "User not found")
    existing = db.query(Subscription).filter(
        Subscription.follower_id == follower.id,
        Subscription.following_id == following_id
    ).first()
    if existing:
        raise HTTPException(400, "Already following")
    sub = Subscription(follower_id=follower.id, following_id=following_id)
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub

def unsubscribe(db: Session, follower: User, following_id: int):
    sub = db.query(Subscription).filter(
        Subscription.follower_id == follower.id,
        Subscription.following_id == following_id
    ).first()
    if not sub:
        raise HTTPException(404, "Subscription not found")
    db.delete(sub)
    db.commit()

def get_followers(db: Session, user_id: int) -> dict:
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    subs = db.query(Subscription).filter(Subscription.following_id == user_id).all()
    users = [sub.follower for sub in subs]
    return {"users": users, "total": len(users)}

def get_following(db: Session, user_id: int) -> dict:
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    subs = db.query(Subscription).filter(Subscription.follower_id == user_id).all()
    users = [sub.following for sub in subs]
    return {"users": users, "total": len(users)}