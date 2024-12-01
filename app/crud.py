from app.models import Event
from sqlmodel import select, text
from sqlalchemy.ext.asyncio import AsyncSession


async def create_event(db: AsyncSession, event: Event):
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event


async def get_event_by_id(db: AsyncSession, event_id: int):
    # result = await db.execute(select(Event).where(Event.id == event_id))
    sql = text("SELECT id, name, date, location, owner_id FROM event WHERE id = :event_id")
    result = await db.execute(sql, {"event_id": event_id})
    event = result.mappings().first()
    if not event:
        return None
    return event


async def get_events(db: AsyncSession, date=None, location=None):
    query = select(Event).order_by(Event.id)
    if date:
        query = query.where(Event.date == date)
    if location:
        query = query.where(Event.location.ilike(f"%{location}%"))

    # Execute the query and retrieve results asynchronously
    result = await db.execute(query)
    events = result.scalars().all()  # Collect the results as a list
    return events
