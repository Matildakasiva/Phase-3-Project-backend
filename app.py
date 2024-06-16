from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from validation_models import DestinationModel, DetailsModel, JournalModel

from models.destination import Destination
from models.details import Details
from models.journal import Journal

app = FastAPI(debug=True)

app.add_middleware(CORSMiddleware, allow_origins = ["*"], allow_credentials = True, allow_methods = ["*"], allow_headers = ["*"])

@app.get('/')
def index():
    return {"Msg": "Hello World."}

@app.get('/destination')
def get_destination():
    destination = Destination.find_all()
    return destination

@app.post('/destination')
def create_destination(data: DestinationModel):
    destination = Destination(data.name, data.image, data.location, data.description)
    destination.save()
    return destination.to_dict()

@app.delete('/destination/{id}')
def delete_destination(id: int):
    destination = Destination.find_by_id(id)
    if destination:
        destination.delete()
        return {"message": "Destination deleted successfully"}
    return {"message": "Deletion not successfull"}

@app.patch('/destination/{id}')
def update_destination(id: int, data: DestinationModel):
    destination = Destination.find_by_id(id)
    if destination:
        destination.name = data.name
        destination.image = data.image
        destination.location = data.location
        destination.description = data.description
        destination.update()
        return {"message": "Destination updated successfully"}
    return {"message": "Destination not found"}, 404


@app.get('/details')
def get_details():
    details = Details.find_all()
    return details


@app.post('/details')
def create_details(data: DetailsModel):
    details = Details(data.name, data.image, data.accomodation, data.attractions, data.festivals, data.vehicle_rentals)
    details.save()

    return details.to_dict()

@app.delete('/details/{id}')
def delete_details(id: int):
    details = Details.find_by_id(id)
    if details:
        details.delete()
        return {"message": "Details deleted successfully"}
    return {"message": "Deletion not successfull"}



@app.get('/journal_entries')
def get_journal():
    journal = Journal.find_all()
    return journal

# searches for a journal entry by title 
@app.get("/journal_entries/search/")
async def search_journal_entries(q: str):
    results = [entry for entry in Journal.find_all() if q in entry.title] 
    if not results:
        return{"message": "Journal title not found."}
    return results

# Creates a new journal entry
@app.post("/journal_entries")
def create_journal_entry(data: JournalModel):
    journal = Journal(data.title, data.content, data.time)
    journal.save()
    Journal.append(journal)
    return journal

#deletes a journal entry
@app.delete("/journal_entries/{id}")
def delete_journal_entry(id: int):
    for entry in Journal:
        if entry.id == id:
            Journal.remove(entry)
            return {"message": "Journal entry deleted successfully"}
    return {"message": "Journal entry not found"}, 404

