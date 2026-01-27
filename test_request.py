import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "http://localhost:8000"

def test_webhook():
    endpoint = f"{BASE_URL}/api/v1/webhook/n8n"
    # If API_KEY is None, it might fail auth, which is a good test case for failure.
    # But here we want to test success.
    headers = {"X-API-KEY": API_KEY if API_KEY else ""}
    
    payload = {
        "elevenlabs_voice_id": "test_voice_id_123",
        "transcript": "This is a test transcript.",
        "audio_url": "https://example.com/audio.mp3"
    }

    print(f"Sending POST request to {endpoint}...")
    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("Test PASSED!")
        else:
            print("Test FAILED! (Status code not 200)")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Is it running?")

if __name__ == "__main__":
    if not API_KEY:
        print("Warning: API_KEY not found in environment.")
    test_webhook()
