from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

class Reservation(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    room_name: str
    start_time: datetime
    end_time: datetime

    @field_validator('end_time')
    def check_times(cls, v, info):
        start = info.data.get('start_time')
        if start and v <= start:
            raise ValueError('Lopetusajan on oltava aloitusaikaa myöhemmin.')
        if v < datetime.now():
            raise ValueError('Varaus ei voi olla menneisyydessä.')
        return v