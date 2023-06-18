from datetime import now

from fastapi import APIRouter, Depends
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from db.database import get_db
from models.models import Notification
from schemas.Notification import (AddNotificationDB, DeleteNotificationDB,
                                  EditNotificationDB, NotificationDB,
                                  UpdateDataNotificationDB)

router = APIRouter(prefix='/notification')


@router.get('/get_notifications', response_model=list[NotificationDB])
async def get_notifications(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    query = select(Notification).offset(skip).limit(limit)
    return await db.execute(query)


@router.post('/add_notification', response_model=NotificationDB)
async def add_notification(*, request: Request, form: AddNotificationDB, db: AsyncSession = Depends(get_db)):
    stmt = insert(Notification).values(*form.dict()).returning(Notification)
    wrap = await db.execute(stmt)
    return wrap


@router.post('/update_notification', response_model=NotificationDB)
async def update_notification(*, request: Request, form: EditNotificationDB, db: AsyncSession = Depends(get_db)):
    v = form.dict()
    del v['id_notification']
    stmt = (update(Notification)
            .values(*v)
            .where(Notification.id_notification == form.id_notification)
            .returning(Notification))
    wrap = await db.execute(stmt)
    return wrap


@router.post('/delete_notification')
async def delete_notification(*, request: Request, form: DeleteNotificationDB, db: AsyncSession = Depends(get_db)):
    stmt = (
        delete(NotificationDB)
        .where(Notification.id_notification == form.id_notification)
    )
    await db.execute(stmt)


@router.post('/update_data_notification')
async def update_data_notification(*, request: Request, form: UpdateDataNotificationDB, db: AsyncSession = Depends(get_db)):
    stmt = (update(Notification)
            .values(last_update=now())
            .where(Notification.id_content == form.id_content))
    await db.execute(stmt)
