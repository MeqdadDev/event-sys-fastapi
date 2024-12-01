from fastapi import FastAPI
from app.database import init_db
from app.routers import auth, events, participants

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(auth.router)
app.include_router(events.router)
app.include_router(participants.router)
