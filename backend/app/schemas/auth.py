from typing import Annotated
from pydantic import BaseModel, Field

class TokenResponse(BaseModel):
    access_token: Annotated[str, Field(description="JWT access-токен (время жизни ~15 мин)")]
    refresh_token: Annotated[str, Field(description="JWT refresh-токен (время жизни 7 дней)")]
    token_type: Annotated[str, Field(default="bearer", description="Тип токена")] = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: Annotated[str, Field(description="Действующий refresh-токен")]


class LogoutRequest(BaseModel):
    refresh_token: Annotated[str, Field(description="Токен для отзыва (внесения в чёрный список)")]