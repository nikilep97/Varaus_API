import requests
from datetime import datetime, timedelta, timezone

BASE_URL = "http://localhost:8000"

def run_test(name, payload, expected_status):
    print(f"--- Testataan: {name} ---")
    try:
        response = requests.post(f"{BASE_URL}/reservations/", json=payload)
        status_code = response.status_code
        
        if status_code == expected_status:
            print(f" OK (Saatiin {status_code})")
            if status_code == 201:
                print(f"   Vastaus: {response.json()}")
            else:
                print(f"   Virheviesti (kuten pitikin): {response.json()['detail'] if 'detail' in response.json() else response.json()}")
        else:
            print(f" VIRHE (Odotettiin {expected_status}, saatiin {status_code})")
            print(f"   Vastaus: {response.text}")
            
    except Exception as e:
        print(f" Yhteysvirhe: {e}")
    print()

# Apumuuttujat ajoille (UTC)
now = datetime.now(timezone.utc)
tomorrow_start = (now + timedelta(days=1)).replace(hour=10, minute=0, second=0, microsecond=0)
tomorrow_end = tomorrow_start + timedelta(hours=1)
yesterday_start = (now - timedelta(days=1)).replace(hour=10, minute=0)
yesterday_end = yesterday_start + timedelta(hours=1)

# 1. Normaali varaus (Huominen 10:00 - 11:00)
valid_reservation = {
    "room_name": "Neukkari 1",
    "start_time": tomorrow_start.isoformat(),
    "end_time": tomorrow_end.isoformat()
}

# 2. Varaus menneisyyteen (Eilinen) - TÄMÄN PITÄISI EPÄONNISTUA
past_reservation = {
    "room_name": "Neukkari 1",
    "start_time": yesterday_start.isoformat(),
    "end_time": yesterday_end.isoformat()
}

# 3. Lopetusaika ennen alkua
invalid_times_reservation = {
    "room_name": "Neukkari 1",
    "start_time": tomorrow_end.isoformat(),
    "end_time": tomorrow_start.isoformat()
}

# 4. Päällekkäinen varaus (Sama kuin valid_reservation) - TÄMÄN PITÄISI EPÄONNISTUA
overlap_reservation = {
    "room_name": "Neukkari 1",
    "start_time": tomorrow_start.isoformat(),
    "end_time": tomorrow_end.isoformat()
}

# Ajetaan testit
if __name__ == "__main__":
    print("Aloitetaan testaus...\n")
    
    # Testi 1: Pitäisi onnistua (201 Created)
    run_test("Valid varaus tulevaisuuteen", valid_reservation, 201)
    
    # Testi 2: Pitäisi epäonnistua (422 Unprocessable Entity - Pydantic validointi)
    run_test("Varaus menneisyyteen", past_reservation, 422)
    
    # Testi 3: Pitäisi epäonnistua (422 Unprocessable Entity)
    run_test("Lopetusaika ennen alkua", invalid_times_reservation, 422)

    # Testi 4: Tämän pitäisi epäonnistua, koska huone "Neukkari 1" varattiin jo testissä 1
    run_test("Päällekkäinen varaus", overlap_reservation, 400)