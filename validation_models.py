from pydantic import BaseModel
from datetime import datetime

class DestinationModel(BaseModel):
    id: int = None
    name: str
    image: str
    location: str
    description: str

class DetailsModel(BaseModel):
    id: int = None
    name: str
    image: str
    attractions: str
    festivals: str
    accomodation: str
    vehicle_rentals: str

class JournalModel(BaseModel):
    id: int = None
    title: str
    content: str
    timestamp: datetime = datetime.now()
