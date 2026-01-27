from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import VoiceLog
import random
import uuid
from datetime import datetime, timedelta

def seed():
    db = SessionLocal()
    
    # Check if data exists
    if db.query(VoiceLog).count() > 0:
        print("Data already exists. Skipping seed.")
        db.close()
        return

    print("Seeding data...")
    
    samples = [
        {
            "transcript": "Client is interested in a complete overhaul of their legacy CRM system. They need better integration with email marketing and automated follow-ups. Budget is around $50k. Timeline is Q3.",
            "voice_id": "JBFqnCBsd6RMkjVDRZzb"
        },
        {
            "transcript": "Meeting with Sarah from TechCorp. They are looking for an AI chatbot to handle customer support L1 queries. Specific focus on reducing response time. Timeline: 3 months. Needs multi-language support.",
            "voice_id": "TxGEqnCsz6RMkjVDRZzb"
        },
        {
            "transcript": "Discussed the new mobile app feature for loyalty points using blockchain. The client wants a gamified experience. Needs UI/UX design and backend implementation ASAP.",
            "voice_id": "XbGEqnCsz6RMkjVDRZxc"
        },
        {
            "transcript": "Proposal needed for a web scraping project. They want to monitor competitor prices daily. Python/Scrapy preferred. Data should be exported to CSV and dashboard.",
            "voice_id": "ErGEqnCsz6RMkjVDRZxy"
        },
        {
            "transcript": "Healthcare client needs a secure patient portal. HIPAA compliance is mandatory. Appointment scheduling and tele-consultation features are required.",
            "voice_id": "PiGEqnCsz6RMkjVDRZxz"
        }
    ]

    for sample in samples:
        log = VoiceLog(
            elevenlabs_voice_id=sample["voice_id"],
            transcript=sample["transcript"],
            audio_url=f"https://example.com/audio/{uuid.uuid4()}.mp3",
            created_at=datetime.now() - timedelta(days=random.randint(0, 5))
        )
        db.add(log)
    
    db.commit()
    print("Seeding complete. Added 5 records.")
    db.close()

if __name__ == "__main__":
    seed()
