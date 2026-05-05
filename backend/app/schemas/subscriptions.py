from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field
from app.schemas.users import UserResponse   # переиспользуем схему пользователя

class SubscriptionResponse(BaseModel):
    id: Annotated[int, Field(ge=1)]
    follower_id: Annotated[int, Field(ge=1, description="Кто подписался")]
    following_id: Annotated[int, Field(ge=1, description="На кого подписались")]
    created_at: Annotated[datetime, Field(description="Дата подписки")]

class SubscriberList(BaseModel):
    users: Annotated[list[UserResponse], Field(description="Список пользователей")]
    total: Annotated[int, Field(ge=0, description="Общее количество")]