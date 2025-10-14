import datetime
import time
import pathlib
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.core.database import engine, Base
from app.api.v1 import admin, user, auth
from app.utils import get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount('/static', StaticFiles(directory='app/static'), name='static')

app.include_router(admin.router, tags=['admin'])
app.include_router(user.router, tags=['dashboard'])
app.include_router(auth.router, tags=['auth'])

log_file_path = pathlib.Path('logs/logs.txt')

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
    else:
        token = None
    username = get_current_user(token).username
    user_agent = request.headers.get('user-agent')
    method = request.method
    path = request.url.path
    response = await call_next(request)
    status_code = response.status_code
    total_time  = time.time() - start
    with open(log_file_path, 'a') as log:
        log.write(f"{datetime.datetime.now()} | {method}, {path} | {user_agent} | "
                  f"user: {username} | time: {total_time:.2f}s | status_code: {status_code}\n")

    return response
