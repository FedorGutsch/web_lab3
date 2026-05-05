from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.post import Post
from app.models.subscription import Subscription
from app.schemas.posts import PostCreate, PostUpdate
from app.models.user import User

def create_post(db: Session, author: User, data: PostCreate) -> Post:
    post = Post(**data.dict(), author_id=author.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    # добавляем удобные поля для сериализации (Pydantic сам подхватит, если атрибуты есть)
    post.author_username = author.username
    post.likes_count = 0
    return post

def update_post(db: Session, post_id: int, current_user: User, data: PostUpdate) -> Post:
    post = db.query(Post).get(post_id)
    if not post:
        raise HTTPException(404, "Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(403, "Not your post")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(post, field, value)
    db.commit()
    db.refresh(post)
    # обновляем вспомогательные поля
    post.author_username = post.author.username
    post.likes_count = len(post.reactions)
    return post

def delete_post(db: Session, post_id: int, current_user: User):
    post = db.query(Post).get(post_id)
    if not post:
        raise HTTPException(404, "Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(403, "Not your post")
    db.delete(post)
    db.commit()

def get_post(db: Session, post_id: int) -> Post:
    post = db.query(Post).get(post_id)
    if not post:
        raise HTTPException(404, "Post not found")
    post.author_username = post.author.username
    post.likes_count = len(post.reactions)
    return post

def _enrich_posts(posts):
    """Добавляет author_username и likes_count списку постов."""
    for p in posts:
        p.author_username = p.author.username
        p.likes_count = len(p.reactions)

def get_feed(db: Session, page: int = 1, size: int = 20) -> dict:
    offset = (page - 1) * size
    posts = db.query(Post).order_by(Post.created_at.desc()).offset(offset).limit(size).all()
    total = db.query(Post).count()
    _enrich_posts(posts)
    return {"posts": posts, "total": total, "page": page, "size": size}

def get_my_posts(db: Session, current_user: User, page: int = 1, size: int = 20) -> dict:
    offset = (page - 1) * size
    posts = db.query(Post).filter(Post.author_id == current_user.id)\
               .order_by(Post.created_at.desc()).offset(offset).limit(size).all()
    total = db.query(Post).filter(Post.author_id == current_user.id).count()
    _enrich_posts(posts)
    return {"posts": posts, "total": total, "page": page, "size": size}

def get_subscription_feed(db: Session, current_user: User, page: int = 1, size: int = 20) -> dict:
    offset = (page - 1) * size
    # получаем список id тех, на кого подписан текущий пользователь
    following_ids = [
        sub.following_id for sub in
        db.query(Subscription).filter(Subscription.follower_id == current_user.id).all()
    ]
    if not following_ids:
        return {"posts": [], "total": 0, "page": page, "size": size}
    posts = db.query(Post).filter(Post.author_id.in_(following_ids))\
               .order_by(Post.created_at.desc()).offset(offset).limit(size).all()
    total = db.query(Post).filter(Post.author_id.in_(following_ids)).count()
    _enrich_posts(posts)
    return {"posts": posts, "total": total, "page": page, "size": size}