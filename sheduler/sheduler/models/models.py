from sheduler.postgres.base_model import BaseModel
from typing import Optional
from sqlalchemy import ForeignKey, Text, String, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime


class Event(BaseModel):
    __tablename__ = 't_event'
    __table_args__ = (
        {'schema': 'notification'}
    )
    id_event: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    last_call: Mapped[datetime] = mapped_column(default=func.now())
    interval: Mapped[int]


class Wrapper(BaseModel):
    __tablename__ = 't_wrapper'
    __table_args__ = (
        {'schema': 'notification'}
    )
    id_wrapper: Mapped[int] = mapped_column(primary_key=True)
    id_event: Mapped[int] = mapped_column(ForeignKey('notification.t_event.id_event'), ondelete="CASCADE")
    template: Mapped[str] = mapped_column(Text)


class Unsubscribe(BaseModel):
    __tablename__ = 't_unsubscribe'
    __table_args__ = (
        {'schema': 'notification'}
    )
    id_unsubscribe: Mapped[int] = mapped_column(primary_key=True)
    id_event: Mapped[int] = mapped_column(ForeignKey('notification.t_event.id_event'), ondelete="CASCADE")
    id_user: Mapped[int]


class Notification(BaseModel):
    __tablename__ = 't_notification'
    __table_args__ = (
        {'schema': 'notification'}
    )
    id_notification: Mapped[int] = mapped_column(primary_key=True)
    id_content: Mapped[Optional[int]]
    id_event: Mapped[int] = mapped_column(ForeignKey('notification.t_event.id_event'), ondelete="CASCADE")
    id_user: Mapped[Optional[int]]
    last_update: Mapped[Optional[datetime]]
    last_notification_send: Mapped[Optional[datetime]]


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
