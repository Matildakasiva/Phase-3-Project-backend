from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from validation_models import DestinationModel, DetailsModel, JournalModel

from models.destination import Destination
from models.details import Details
from models.journaling import Journaling

app = FastAPI(debug=True)

app.add_middleware(CORSMiddleware, allow_origins = ["*"], allow_credentials = True, allow_methods = ["*"], allow_headers = ["*"])

@app.get('/')
def index():
    return {"Msg": "Hello World."}


#destination

@app.get('/destination')
def get_destination():
    destination = Destination.find_all()
    return destination

#updates
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

#edits
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

#destination details

#gets all
@app.get('/details')
def get_details():
    details = Details.find_all()
    return details

#gets by id
@app.get('/details/{id}')
def get_detail(id: int):
    detail = Details.find_by_id(id)
    return detail

#updates
@app.post('/details')
def create_details(data: DetailsModel):
    details = Details(data.name, data.image, data.accomodation, data.attractions, data.festivals, data.vehicle_rentals)
    details.save()

    return details.to_dict()

#deletes
@app.delete('/details/{id}')
def delete_details(id: int):
    details = Details.find_by_id(id)
    if details:
        details.delete()
        return {"message": "Details deleted successfully"}
    return {"message": "Deletion not successfull"}


 # Journal
@app.get('/journal_entries')
def get_journal():
    journal = Journaling.find_all()
    return journal

#edits
@app.patch('/journal_entries/{id}')
def update_entry(id: int, data: JournalModel):
    entry = Journaling.find_by_id(id)
    if entry:
        entry.title = data.title
        entry.content = data.content
        entry.timestamp = data.timestamp
        entry.update()
        return {"message": "entry updated successfully"}
    return {"message": "entry not found"}, 404


# Creates a new journal entry
@app.post("/journal_entries")
def create_journal_entry(data: JournalModel):
    journal = Journaling(data.title, data.content)
    journal.save()

#deletes a journal entry
@app.delete("/journal_entries/{id}")
def delete_journal_entry(id: int):
    entry = Journaling.find_by_id(id)
    if entry:
        entry.delete()
        return{"message": "Entry successfully deleted"}
    return {"message": "Deletion not successfull"}

