from pydantic import BaseModel

class DestinationModel(BaseModel):
    id: int
    name: str
    image: str
    location: str
    description: str

class DetailsModel(BaseModel):
    id: int
    name: str
    image: str
    attractions: str
    festivals: str
    accomodation: str
    vehicle_rentals: str

class JournalModel(BaseModel):
    id: int
    title: str
    content: str
    time: int
