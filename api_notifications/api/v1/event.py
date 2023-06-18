from fastapi import APIRouter, Depends
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from db.database import get_db
from models.models import Event
from schemas.Event import AddEventDB, DeleteEventDB, EditEventDB, EventDB

router = APIRouter(prefix='/event')


@router.get('/get_events', response_model=list[EventDB])
async def get_events(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    query = select(Event).offset(skip).limit(limit)
    return await db.execute(query)


@router.post('/add_event', response_model=EventDB)
async def add_event(*, request: Request, form: AddEventDB, db: AsyncSession = Depends(get_db)):
    stmt = insert(Event).values(*form.dict()).returning(Event)
    ev = await db.execute(stmt)
    return ev


@router.post('/update_event', response_model=EventDB)
async def update_event(*, request: Request, form: EditEventDB, db: AsyncSession = Depends(get_db)):
    v = form.dict()
    del v['id_event']
    stmt = (update(Event)
            .values(*v)
            .where(Event.id_event == form.id_event)
            .returning(Event))
    ev = await db.execute(stmt)
    return ev


@router.post('/delete_event')
async def delete_event(*, request: Request, form: DeleteEventDB, db: AsyncSession = Depends(get_db)):
    stmt = (
        delete(EventDB)
        .where(Event.id_event == form.id_event)
    )
    await db.execute(stmt)
