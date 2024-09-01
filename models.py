from pydantic import BaseModel
class Token(BaseModel):
    access_token: str
    token_type: str

# модели данных
class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    pass

class NoteInDB(NoteBase):
    id: int
    username: str

class User(BaseModel):
    username: str
    password: str

class UserInDB(BaseModel):
    hashed_password: str