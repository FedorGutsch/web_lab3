from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field

class PostBase(BaseModel):
    title: Annotated[
        str,
        Field(
            min_length=1,
            max_length=200,
            examples=["Мой первый пост"],
            description="Заголовок поста"
        )
    ]
    content: Annotated[
        str,
        Field(
            min_length=1,
            max_length=5000,
            examples=["Сегодня я начал изучать FastAPI..."],
            description="Текст поста"
        )
    ]
    image_url: Annotated[
        str | None,
        Field(
            None,
            max_length=2048,
            examples=["https://site.com/uploads/post123.jpg"],
            description="Ссылка на изображение (опционально)"
        )
    ] = None

class PostCreate(PostBase):
    """Используется при создании нового поста."""
    pass

class PostUpdate(BaseModel):
    """Все поля необязательные – можно передать только то, что меняем."""
    title: Annotated[
        str | None,
        Field(
            None,
            min_length=1,
            max_length=200,
            description="Новый заголовок"
        )
    ] = None
    content: Annotated[
        str | None,
        Field(
            None,
            min_length=1,
            max_length=5000,
            description="Новое содержимое"
        )
    ] = None
    image_url: Annotated[
        str | None,
        Field(
            None,
            max_length=2048,
            description="Новая ссылка на изображение"
        )
    ] = None

class PostResponse(PostBase):
    id: Annotated[int, Field(ge=1, description="ID поста")]
    author_id: Annotated[int, Field(ge=1, description="ID автора")]
    author_username: Annotated[str, Field(description="Имя автора для отображения")]
    likes_count: Annotated[int, Field(ge=0, description="Количество лайков")] = 0
    created_at: Annotated[datetime, Field(description="Дата создания (UTC)")]
    updated_at: Annotated[datetime, Field(description="Дата последнего обновления (UTC)")]