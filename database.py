from typing import Dict, List, Optional
from uuid import UUID
from threading import Lock
from schemas import Reservation

# In-memory "tietokanta" (id -> Reservation)
db: Dict[UUID, Reservation] = {}
# Lukko estämään samanaikaiset kirjoitukset
db_lock = Lock()

def check_overlap(room_name: str, start_time, end_time) -> bool:
    """Tarkistaa, onko huoneessa päällekkäisiä varauksia."""
    for res in db.values():
        if res.room_name == room_name:
            # Logiikka: (Alku A < Loppu B) JA (Loppu A > Alku B)
            if start_time < res.end_time and end_time > res.start_time:
                return True
    return False

# Yhdistää tarkistuksen ja lisäyksen turvallisesti
def add_reservation_safe(reservation: Reservation) -> Reservation:
    with db_lock:
        # Tarkistetaan päällekkäisyys nyt, kun kukaan muu ei voi kirjoittaa
        if check_overlap(reservation.room_name, reservation.start_time, reservation.end_time):
             # Palautetaan None tai nostetaan virhe, jos päällekkäinen
            raise ValueError("Overlap detected")
            
        db[reservation.id] = reservation
        return reservation

def add_reservation(reservation: Reservation) -> Reservation:
    db[reservation.id] = reservation
    return reservation

def get_all_reservations() -> List[Reservation]:
    return list(db.values())

def get_reservations_by_room(room_name: str) -> List[Reservation]:
    return [r for r in db.values() if r.room_name == room_name]

def get_reservation_by_id(res_id: UUID) -> Optional[Reservation]:
    return db.get(res_id)

def delete_reservation(res_id: UUID) -> bool:
    with db_lock:
        if res_id in db:
            del db[res_id]
            return True
        return False