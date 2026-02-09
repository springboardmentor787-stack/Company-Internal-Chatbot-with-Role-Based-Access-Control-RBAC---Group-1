from fastapi import FastAPI
from backend.auth_routes import router as auth_router
from backend.chat_routes import router as chat_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(chat_router)
