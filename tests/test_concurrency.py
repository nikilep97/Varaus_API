import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import threading
from datetime import datetime, timedelta, timezone

BASE_URL = "http://localhost:8000"

def make_reservation(thread_id, room_name, start, end):
    payload = {
        "room_name": room_name,
        "start_time": start,
        "end_time": end
    }
    try:
        response = requests.post(f"{BASE_URL}/reservations/", json=payload)
        print(f"Säie {thread_id}: Status {response.status_code} - {response.json().get('detail', 'Success')}")
    except Exception as e:
        print(f"Säie {thread_id}: Virhe {e}")

if __name__ == "__main__":
    print("--- Aloitetaan samanaikaisuustesti (Race Condition) ---")
    
    # Määritellään ajat (UTC)
    now = datetime.now(timezone.utc)
    start_time = (now + timedelta(days=2)).isoformat() # Kahden päivän päästä
    end_time = (now + timedelta(days=2, hours=1)).isoformat()
    room = "Conference Room A"

    threads = []
    # Luodaan 5 säiettä, jotka kaikki yrittävät varata saman huoneen samaan aikaan
    for i in range(5):
        t = threading.Thread(target=make_reservation, args=(i, room, start_time, end_time))
        threads.append(t)

    # Käynnistetään säikeet
    for t in threads:
        t.start()

    # Odotetaan kaikkien valmistumista
    for t in threads:
        t.join()
        
    print("\nTesti valmis. Vain YHDEN pitäisi onnistua (201), muiden epäonnistua (400).")