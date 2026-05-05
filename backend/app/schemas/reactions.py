from datetime import datetime
from enum import Enum
from typing import Annotated
from pydantic import BaseModel, Field

class ReactionType(str, Enum):
    """Возможные типы реакций."""
    like = "like"
    heart = "heart"
    fire = "fire"
    smile = "smile"

class ReactionCreate(BaseModel):
    reaction_type: Annotated[
        ReactionType,
        Field(examples=["like"], description="Тип реакции из предопределённого списка")
    ]

class ReactionResponse(BaseModel):
    id: Annotated[int, Field(ge=1)]
    user_id: Annotated[int, Field(ge=1)]
    post_id: Annotated[int, Field(ge=1)]
    reaction_type: ReactionType
    created_at: Annotated[datetime, Field(description="Когда реакция была поставлена")]