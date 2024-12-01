# app/routers/events.py

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime
from sqlmodel import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import EventCreate, EventRead
from app.models import Event, User
from app.database import get_session
from app.dependencies import get_current_user
from app.crud import create_event, get_event_by_id, get_events

router = APIRouter()


@router.post("/events", response_model=EventRead, status_code=status.HTTP_201_CREATED)
async def create_new_event(event: EventCreate, db: AsyncSession = Depends(get_session),
                           current_user: User = Depends(get_current_user)):
    new_event = Event(**event.dict(), owner_id=current_user.id)
    return await create_event(db, new_event)


@router.get("/events", response_model=List[EventRead])
async def list_events(date: Optional[datetime] = None, location: Optional[str] = None,
                      db: AsyncSession = Depends(get_session)):
    return await get_events(db, date, location)


@router.get("/events/{event_id}", response_model=EventRead)
async def read_event(event_id: int, db: AsyncSession = Depends(get_session)):
    event = await get_event_by_id(db, event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event


@router.put("/events/{event_id}", response_model=EventRead)
async def update_event(event_id: int, event: EventCreate, db: AsyncSession = Depends(get_session),
                       current_user: User = Depends(get_current_user)):
    db_event = await get_event_by_id(db, event_id)
    if not db_event or db_event.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this event")

    for key, value in event.dict().items():
        setattr(db_event, key, value)
    await db.commit()
    await db.refresh(db_event)
    return db_event


@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id: int, db: AsyncSession = Depends(get_session),
                       current_user: User = Depends(get_current_user)):
    db_event = await get_event_by_id(db, event_id)
    if not db_event or db_event.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this event")

    await db.delete(db_event)
    await db.commit()
    return {"message": "Event deleted successfully"}
