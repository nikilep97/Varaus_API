from fastapi import FastAPI, HTTPException, status
from typing import List
from uuid import UUID
import database
from schemas import Reservation

app = FastAPI(title="Kokoushuoneiden varausjärjestelmä")

@app.post("/reservations/", response_model=Reservation, status_code=status.HTTP_201_CREATED)
def create_reservation(reservation: Reservation):
    # Tarkistetaan päällekkäisyys ennen tallennusta
    try:
        saved_reservation = database.add_reservation_safe(reservation)
        return saved_reservation
    except ValueError:
        raise HTTPException(
            status_code=400, 
            detail=f"Huone {reservation.room_name} on jo varattu kyseisenä aikana."
        ) 

@app.get("/reservations/", response_model=List[Reservation])
def read_reservations(room_name: str = None):
    if room_name:
        return database.get_reservations_by_room(room_name)
    return database.get_all_reservations()

@app.delete("/reservations/{reservation_id}")
def remove_reservation(reservation_id: UUID):
    success = database.delete_reservation(reservation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Varausta ei löytynyt.")
    return {"message": f"Varaus {reservation_id} peruttu onnistuneesti."}