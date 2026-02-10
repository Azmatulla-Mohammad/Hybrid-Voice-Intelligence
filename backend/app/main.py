from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .services.skill_router import SkillRouter
from .core.config import settings
from .core.database import engine, Base
from .models import sql

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    return await SkillRouter.route(request.message)

@app.get("/")
def read_root():
    return {"status": "online", "system": "EDITH", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
