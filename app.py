from fastapi import FastAPI
from models.destination import Destination
from models.details import Details
from models.journal import Journal

app = FastAPI()

@app.get('/')
def index():
    return {"Msg": "Hello World."}

@app.get('/destination')
def get_destination():
    destination = Destination.find_all()

    return destination


@app.get('/details')
def get_details():
    details = Details.find_all()

    return details

@app.get('/journal_entries')
def get_journal():
    journal = Journal.find_all()
    return journal

# searches for a journal entry by title 
@app.get("/journal_entries/search/")
async def search_journal_entries(q: str):
    results = [entry for entry in Journal if q in entry.title] 
    if not results:
        return{"message": "Journal title not found."}
    return results

# Creates a new journal entry
@app.post("/journal_entries/")
def create_journal_entry(journal_entry: Journal):
    Journal.append(journal_entry)
    return journal_entry

#deletes a journal entry
@app.delete("/journal_entries/{id}")
def delete_journal_entry(id: int):
    for entry in Journal:
        if entry.id == id:
            Journal.remove(entry)
            return {"message": "Journal entry deleted successfully"}
    return {"message": "Journal entry not found"}, 404

