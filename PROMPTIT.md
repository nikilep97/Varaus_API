Toimi junior-tason ohjelmistokehittäjänä. Tehtävänäsi on toteuttaa yksinkertainen kokoushuoneiden varausrajapinta käyttäen Python ja FastAPI.

Toteuta seuraavat ominaisuudet:
1. Varauksen luonti: Huoneen varaaminen tietylle aikavälille.
2. Varauksen peruutus: Olemassa olevan varauksen poistaminen.
3. Varausten katselu: Listaa kaikki tietyn huoneen varaukset.

Tekniset vaatimukset:
1. Käytä tallennukseen muistinvaraista tietokantaa (in-memory).
2. Varmista, että varaukset eivät mene päällekkäin.
3. Varmista, että varaukset eivät ole menneisyydessä ja että aloitusaika on ennen lopetusaikaa.

Kirjoita selkeää koodia ja selitä lyhyesti, miten toteutit varauslogiikan.



Moi! Tässä olisi ehdotukseni varausrajapinnaksi. Junior-kehittäjänä panostin koodin luettavuuteen ja siihen, että virhetilanteet (kuten päällekkäiset varaukset) palauttavat selkeät viestit käyttäjälle.

Käytän tallennukseen Pythonin sanakirjaa (`dict`), jossa avaimena on huoneen nimi ja arvona lista varausolioita.

### Kooditoteutus (FastAPI)

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import List, Dict

app = FastAPI(title="Kokoushuoneiden varausjärjestelmä")

# Tietomalli varaukselle
class Reservation(BaseModel):
    room_name: str
    start_time: datetime
    end_time: datetime

    @field_validator('end_time')
    @classmethod
    def check_times(cls, v, info):
        start = info.data.get('start_time')
        if start and v <= start:
            raise ValueError('Lopetusajan on oltava aloitusaikaa myöhemmin.')
        if v < datetime.now():
            raise ValueError('Varaus ei voi olla menneisyydessä.')
        return v

# In-memory "tietokanta"
db: Dict[str, List[Reservation]] = {}

@app.post("/reservations/", status_code=status.HTTP_201_CREATED)
def create_reservation(res: Reservation):
    # Luodaan huone listaan, jos sitä ei vielä ole
    if res.room_name not in db:
        db[res.room_name] = []
    
    # Tarkistetaan päällekkäisyydet
    for existing in db[res.room_name]:
        # Logiikka: (Alku A < Loppu B) JA (Loppu A > Alku B)
        if res.start_time < existing.end_time and res.end_time > existing.start_time:
            raise HTTPException(
                status_code=400, 
                detail=f"Huone {res.room_name} on jo varattu kyseisenä aikana."
            )
    
    db[res.room_name].append(res)
    return {"message": "Varaus onnistui", "data": res}

@app.get("/reservations/{room_name}", response_model=List[Reservation])
def get_reservations(room_name: str):
    return db.get(room_name, [])

@app.delete("/reservations/{room_name}")
def cancel_reservation(room_name: str, start_time: datetime, end_time: datetime):
    if room_name not in db:
        raise HTTPException(status_code=404, detail="Huonetta ei löytynyt.")
    
    original_count = len(db[room_name])
    # Suodatetaan pois varaus, joka täsmää annettuihin aikoihin
    db[room_name] = [
        r for r in db[room_name] 
        if not (r.start_time == start_time and r.end_time == end_time)
    ]
    
    if len(db[room_name]) == original_count:
        raise HTTPException(status_code=404, detail="Varausta ei löytynyt annetuilla ajoilla.")
        
    return {"message": "Varaus peruttu onnistuneesti."}

```

---

### Miten toteutin varauslogiikan?

Toteutuksessa on kolme tärkeää tarkistuspistettä:

1. **Ajan validointi:** Käytin Pydanticin `field_validatoria`. Se tarkistaa jo ennen kuin koodi ehtii logiikkaan asti, että varaus ei ole menneisyydessä ja että `end_time` on loogisesti aloituksen jälkeen.
2. **Päällekkäisyyksien esto:** Tämä on varausjärjestelmien "pihvi". Käytin kaavaa, jossa kaksi aikaväliä leikkaa, jos **uuden varauksen alku on ennen vanhan loppua** JA **uuden varauksen loppu on vanhan alun jälkeen**. Tämä kattaa kaikki skenaariot: osittaiset päällekkäisyydet, sisäkkäiset varaukset ja täsmälleen samat ajat.
3. **Tallennus:** Koska kyseessä on in-memory-toteutus, käytin sanakirjaa, jossa huoneen nimi toimii avaimena. Tämä tekee tietyn huoneen varausten hakemisesta nopeampaa kuin jos kävisimme läpi yhtä jättimäistä listaa.

Haluaisitko, että lisään tähän vielä automaattiset testit (pytest), joilla varmistetaan, että nuo aikojen päällekkäisyydet todella estetään?