# app/routers/participants.py

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.schemas import ParticipantCreate
from app.models import Participant, User
from app.database import get_session
from app.dependencies import get_current_user
from app.crud import get_event_by_id

router = APIRouter()


@router.post("/participants", status_code=status.HTTP_201_CREATED)
async def add_participant(
    participant: ParticipantCreate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    event = await get_event_by_id(db, participant.event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )

    existing_participant = await db.execute(
        select(Participant).where(
            Participant.event_id == participant.event_id,
            Participant.user_id == participant.user_id,
        )
    )

    participant_exists = existing_participant.scalar_one_or_none()

    if participant_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already a participant in this event",
        )

    new_participant = Participant(
        event_id=participant.event_id, user_id=participant.user_id
    )
    db.add(new_participant)
    await db.commit()
    await db.refresh(new_participant)
    return {"message": "Participant added successfully"}


@router.get("/events/{event_id}/participants", response_model=List[ParticipantCreate])
async def list_participants(event_id: int, db: AsyncSession = Depends(get_session)):
    event = await get_event_by_id(db, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )

    result = await db.execute(
        select(Participant).where(Participant.event_id == event_id)
    )
    participants = result.scalars().all()
    return participants
