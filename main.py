from routes.tasks import tasks_router
from fastapi import FastAPI
from config.db import init_db

app = FastAPI()


@app.on_event("startup")
async def connect_db():
    await init_db()


app.include_router(tasks_router, prefix="/tasks")
