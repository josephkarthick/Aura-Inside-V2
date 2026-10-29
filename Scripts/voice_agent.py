# voice_agent.py
import requests
import pyttsx3
import time
from datetime import datetime

API_URL = "http://192.168.5.27:8000/auravoice/api/announcements/"
CHECK_INTERVAL = 60  # seconds

def speak(text, voice_name=None, rate=1.0):
    import pyttsx3
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    selected = None
    print(f"🎙️ Requested voice (contains): {voice_name}")

    for v in voices:
        print(f"🔍 Available voice: {v.name} (ID: {v.id})")
        # Use partial match
        if voice_name and voice_name.lower() in v.name.lower():
            engine.setProperty('voice', v.id)
            selected = v.name
            print(f"✅ Selected voice: {v.name}")
            break

    if not selected:
        print(f"⚠️ Voice containing '{voice_name}' not found. Using default.")

    engine.setProperty('rate', int(rate * 150))  # 1.0 = 150 wpm
    engine.say(text)
    engine.runAndWait()


def fetch_and_play():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            announcements = response.json()
            if not announcements:
                print(f"[⏳] {datetime.now().strftime('%H:%M')} No announcements.")
            for ann in announcements:
                msg = f"{ann['title']}. {ann['description']}"
                print(f"[🔊] {datetime.now().strftime('%H:%M')} Playing: {msg}")
                speak(msg, ann.get('voice_name'), ann.get('voice_rate', 1.0))
        else:
            print(f"[⚠️] API Error: {response.status_code}")
    except Exception as e:
        print(f"[❌] Exception: {e}")

if __name__ == "__main__":
    print("✅ Voice agent started.")
    while True:
        fetch_and_play()
        time.sleep(CHECK_INTERVAL)
