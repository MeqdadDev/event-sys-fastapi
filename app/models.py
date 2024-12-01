from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    events: List["Event"] = Relationship(back_populates="owner")
    participants: List["Participant"] = Relationship(back_populates="user")

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    date: datetime
    location: str = Field(index=True)
    owner_id: int = Field(foreign_key="user.id")
    owner: User = Relationship(back_populates="events")
    participants: List["Participant"] = Relationship(back_populates="event")

class Participant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="event.id")
    user_id: int = Field(foreign_key="user.id")
    event: Event = Relationship(back_populates="participants")
    user: User = Relationship(back_populates="participants")
