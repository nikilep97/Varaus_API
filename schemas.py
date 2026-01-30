from pydantic import BaseModel, Field, model_validator
from datetime import datetime, timezone
from uuid import UUID, uuid4

class Reservation(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    room_name: str
    start_time: datetime
    end_time: datetime

    @model_validator(mode='after')
    def check_dates(self):
        # Määritellään nykyhetki UTC-ajassa
        now = datetime.now(timezone.utc)
        
        # Varmistetaan, että aikaleimat ovat vertailukelpoisia
        # Jos syöte ei sisällä aikavyöhykettä, Pydantic/FastAPI saattaa käsitellä sen eri tavalla
        start = self.start_time
        if start.tzinfo is None:
            start = start.replace(tzinfo=timezone.utc)
            
        end = self.end_time
        if end.tzinfo is None:
            end = end.replace(tzinfo=timezone.utc)

        # Tarkistus 1: Varaus ei saa alkaa menneisyydessä
        # Sallitaan pieni liukuma (esim. sekunteja), mutta tässä tiukka raja
        if start < now:
            raise ValueError('Varaus ei voi alkaa menneisyydessä.')

        # Tarkistus 2: Lopetusaika on aloituksen jälkeen
        if end <= start:
            raise ValueError('Lopetusajan on oltava aloitusaikaa myöhemmin.')

        return self