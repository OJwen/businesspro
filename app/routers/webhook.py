from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import VoiceLog
from ..schemas import VoiceLogCreate
from ..dependencies import verify_api_key

router = APIRouter()

@router.post("/n8n", status_code=status.HTTP_200_OK)
def create_voice_log(
    voice_log: VoiceLogCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    # Create model. Using model_dump() for Pydantic v2 support
    # (Checking if model_dump exists, else fallback to dict just in case of v1 environment, though v2 is installed)
    if hasattr(voice_log, 'model_dump'):
        data = voice_log.model_dump()
    else:
        data = voice_log.dict()
        
    db_voice_log = VoiceLog(**data)
    
    db.add(db_voice_log)
    db.commit()
    db.refresh(db_voice_log)
    
    return {"status": "success", "id": db_voice_log.id}
