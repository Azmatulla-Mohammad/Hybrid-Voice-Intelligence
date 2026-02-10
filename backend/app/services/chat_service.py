from sqlalchemy.orm import Session
from ..models.sql import Message
from ..core.database import SessionLocal

class ChatService:
    @staticmethod
    def add_message(role: str, content: str):
        db: Session = SessionLocal()
        try:
            msg = Message(role=role, content=content)
            db.add(msg)
            db.commit()
            db.refresh(msg)
            return msg
        finally:
            db.close()

    @staticmethod
    def get_recent_history(limit: int = 5):
        db: Session = SessionLocal()
        try:
            # Get last N messages
            messages = db.query(Message).order_by(Message.id.desc()).limit(limit).all()
            return messages[::-1] # Return in chronological order
        finally:
            db.close()

    @staticmethod
    def format_history_for_gemini(limit: int = 5):
        msgs = ChatService.get_recent_history(limit)
        history = []
        for m in msgs:
            role = "user" if m.role == "user" else "model"
            history.append({"role": role, "parts": [m.content]})
        return history
