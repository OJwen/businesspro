from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from .database import Base

class VoiceLog(Base):
    __tablename__ = "voice_logs"

    id = Column(Integer, primary_key=True, index=True)
    elevenlabs_voice_id = Column(String, index=True)
    transcript = Column(Text)
    audio_url = Column(String)
    client_name = Column(String, default="Client")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
