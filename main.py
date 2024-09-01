from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List
from models import NoteBase, NoteCreate, NoteInDB, Token, User
from auth import login_for_access_token, register_user, get_current_user
from utils import read_data, write_data, check_spelling

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@app.post('/token/', response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return login_for_access_token(form_data)

@app.post("/register/", status_code=status.HTTP_201_CREATED)
def register(body: User) -> dict:
    return register_user(body)

@app.get('/notes/', response_model=List[NoteInDB])
def read_notes(current_user: User = Depends(get_current_user)) -> List[NoteInDB]:
    data = read_data()
    user_notes = [note for note in data["notes"] if note["username"] == current_user.username]
    return user_notes

@app.post("/notes/", response_model=NoteInDB)
def create_note(note: NoteCreate, current_user: User = Depends(get_current_user)) -> NoteInDB:
    data = read_data()
    note_id = len(data["notes"]) + 1
    note_data = note.dict()

    note_data['title'] = check_spelling(note_data['title'])
    note_data['content'] = check_spelling(note_data['content'])

    note_data.update({"id": note_id, "username": current_user.username})
    data["notes"].append(note_data)
    write_data(data)
    return note_data