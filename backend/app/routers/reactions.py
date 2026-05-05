from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_current_user
from app.models.user import User
from app.database.session import get_db
from app.schemas.reactions import ReactionCreate, ReactionResponse
from app.services import reaction as reaction_service

router = APIRouter(prefix="/posts", tags=["reactions"])

@router.post("/{post_id}/reactions", response_model=ReactionResponse, status_code=201)
def add_reaction(post_id: int, data: ReactionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return reaction_service.add_reaction(db, post_id, current_user, data.reaction_type)

@router.delete("/{post_id}/reactions", status_code=204)
def remove_reaction(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    reaction_service.remove_reaction(db, post_id, current_user)
    return

@router.get("/{post_id}/reactions", response_model=list[ReactionResponse])
def get_reactions(post_id: int, db: Session = Depends(get_db)):
    return reaction_service.get_reactions(db, post_id)