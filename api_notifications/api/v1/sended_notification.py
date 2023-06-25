from datetime import datetime

from db.broker import get_brokers
from db.database import get_db
from fastapi import APIRouter, Depends
from schemas.SendedNotification import DeleteSendedNotification
from sqlalchemy import delete, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from api_notifications.models.models import SendedNotification
from api_notifications.schemas.SendedNotification import (
    AddSendedNotification, CheckSendedNotification, SendedNotificationDB)

router = APIRouter(prefix='/sended_notification')


@router.post('/add_sended_notification')
async def add_sended_notification(*, form: AddSendedNotification, db: AsyncSession = Depends(get_db)):
    stmt = insert(SendedNotification).values(*form.dict()).returning(SendedNotification)
    wrap = await db.execute(stmt)
    return wrap


@router.post('/delete_sended_notification', response_model=SendedNotificationDB)
async def delete_sended_notification(*, form: DeleteSendedNotification, db: AsyncSession = Depends(get_db)):
    stmt = (
        delete(SendedNotification)
        .where(SendedNotification.id_sended_notification == form.id_sended_notification)
    )
    await db.execute(stmt)

@router.post('/check_sended_notification')
async def check_sended_notification(*, form: CheckSendedNotification, db: AsyncSession = Depends(get_db)):
    stmt = (update(SendedNotification)
            .values(last_update=datetime.now())
            .where(SendedNotification.id_sended_notification == form.id_sended_notification))
    await db.execute(stmt)
