from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VoiceLogBase(BaseModel):
    elevenlabs_voice_id: str
    transcript: str
    audio_url: str

class VoiceLogCreate(VoiceLogBase):
    pass

class VoiceLogRead(VoiceLogBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
