from fastapi import FastAPI
from app.database.session import engine
from app.models.base import Base
from app.routers import auth, users, posts, subscriptions, reactions

app = FastAPI(title="Social API", version="1.0.0")

# Создаём все таблицы (для разработки, в прод — Alembic)
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(subscriptions.router)
app.include_router(reactions.router)