from typing import Dict, List, Optional
from uuid import UUID
from schemas import Reservation

# In-memory "tietokanta" (id -> Reservation)
db: Dict[UUID, Reservation] = {}

def check_overlap(room_name: str, start_time, end_time) -> bool:
    """Tarkistaa, onko huoneessa päällekkäisiä varauksia."""
    for res in db.values():
        if res.room_name == room_name:
            # Logiikka: (Alku A < Loppu B) JA (Loppu A > Alku B)
            if start_time < res.end_time and end_time > res.start_time:
                return True
    return False

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
    if res_id in db:
        del db[res_id]
        return True
    return False