from base_model import BaseModel
from typing import Optional
from sqlalchemy import Text, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime


class SendedNotification(BaseModel):
    __tablename__ = 't_sended_notification'
    __table_args__ = (
        {'schema': 'notification'}
    )
    id_sended_notification: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int]
    type_notification: Mapped[str]
    message: Mapped[str] = mapped_column(Text)
    date_send: Mapped[datetime] = mapped_column(default=func.now())
    date_check: Mapped[Optional[datetime]]
