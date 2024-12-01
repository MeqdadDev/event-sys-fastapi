from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class EventCreate(BaseModel):
    name: str
    date: datetime
    location: str

class EventRead(BaseModel):
    id: int
    name: str
    date: datetime
    location: str

class ParticipantCreate(BaseModel):
    event_id: int
    user_id: int
