from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.reaction import Reaction, ReactionType
from app.models.post import Post
from app.models.user import User

def add_reaction(db: Session, post_id: int, user: User, reaction_type: ReactionType) -> Reaction:
    post = db.query(Post).get(post_id)
    if not post:
        raise HTTPException(404, "Post not found")
    existing = db.query(Reaction).filter(
        Reaction.user_id == user.id,
        Reaction.post_id == post_id
    ).first()
    if existing:
        # заменяем тип реакции
        existing.reaction_type = reaction_type
        db.commit()
        db.refresh(existing)
        return existing
    reaction = Reaction(
        user_id=user.id,
        post_id=post_id,
        reaction_type=reaction_type
    )
    db.add(reaction)
    db.commit()
    db.refresh(reaction)
    return reaction

def remove_reaction(db: Session, post_id: int, user: User):
    reaction = db.query(Reaction).filter(
        Reaction.user_id == user.id,
        Reaction.post_id == post_id
    ).first()
    if not reaction:
        raise HTTPException(404, "Reaction not found")
    db.delete(reaction)
    db.commit()

def get_reactions(db: Session, post_id: int) -> list[Reaction]:
    post = db.query(Post).get(post_id)
    if not post:
        raise HTTPException(404, "Post not found")
    return db.query(Reaction).filter(Reaction.post_id == post_id).all()