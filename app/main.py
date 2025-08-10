from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import engine, Base
from routes import dashboard, admin

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount('/static', StaticFiles(directory='app/static'), name='static')

app.include_router(admin.router, tags=['admin'])
app.include_router(dashboard.router, tags=['dashboard'])


