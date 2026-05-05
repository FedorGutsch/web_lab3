from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    username: Annotated[
        str,
        Field(
            min_length=3,
            max_length=30,
            pattern=r'^[a-zA-Z0-9_]+$',
            examples=['john_doe'],
            description='Уникальное имя пользователя (только латиница, цифры, подчёркивание)'
        )
    ]
    email: Annotated[EmailStr, Field(
        examples=['user@example.com'],
        description='Email пользователя'
    )]

class UserCreate(UserBase):
    password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=128,
            examples=['SecureP@ss1'],
            description='Пароль (мин. 8 символов)'
        )
    ]

class UserLogin(BaseModel):
    email: EmailStr = Field(examples=['user@example.com'])
    password: str = Field(min_length=8, max_length=128, examples=['SecureP@ss1'])

class UserUpdate(BaseModel):
    username: Annotated[
        str | None,
        Field(
            None,
            min_length=3,
            max_length=30,
            pattern=r'^[a-zA-Z0-9_]+$',
            examples=['new_john'],
            description='Новое имя пользователя'
        )
    ]
    email: EmailStr | None = Field(None, examples=['new_email@example.com'])
    bio: Annotated[
        str | None,
        Field(None, max_length=500, examples=['Привет, я разработчик!'])
    ]
    avatar_url: Annotated[
        str | None,
        Field(None, max_length=2048, examples=['https://site.com/ava.jpg'])
    ]

class UserResponse(UserBase):
    id: int = Field(..., ge=1, description='ID пользователя')
    bio: str | None = Field(None, max_length=500)
    avatar_url: str | None = Field(None, max_length=2048)
    created_at: datetime = Field(..., description='Дата регистрации (UTC)')

class UserSearchResponse(BaseModel):
    users: list[UserResponse]
    total: int = Field(..., ge=0, description='Всего найдено пользователей')