from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.database import engine, Base
from app.api.v1 import admin, user, auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount('/static', StaticFiles(directory='app/static'), name='static')

app.include_router(admin.router, tags=['admin'])
app.include_router(user.router, tags=['dashboard'])
app.include_router(auth.router, tags=['auth'])


