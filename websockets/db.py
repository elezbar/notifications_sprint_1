from abc import ABCMeta, abstractmethod
from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import db_url
from models import SendedNotification

Base = declarative_base()

engine = create_engine(db_url)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)


def session(func):
    def wrapper(*args, **kwargs):
        wrapper.__annotations__ = func.__annotations__
        wrapper.__doc__ = func.__doc__
        with DBSession() as session:
            try:
                return func(*args, **kwargs, session=session)
            except Exception as e:
                session.rollback()
                raise e
    return wrapper


class DBhandlersABC(metaclass=ABCMeta):

    @abstractmethod
    def request_notifications(self, user_id: int) -> list[SendedNotification] | None:
        """Делает запрос новых уведомлений."""
        pass

    @abstractmethod
    def renew_notification(self, notification: SendedNotification) -> None:
        """Обновляет дату уведомления в БД."""
        pass


class DBhandlers(DBhandlersABC):

    @session
    def __init__(self, session):
        self.session = session

    def request_notifications(self, user_id: int) -> list[SendedNotification] | None:
        stmt = (
            select(SendedNotification)
            .where(SendedNotification.id_user == user_id)
            .where(SendedNotification.type_notification == 'websocket')
            .where(SendedNotification.date_check == None)
        )
        return self.session.scalars(stmt)

    def renew_notification(self, notification: SendedNotification) -> None:
        notification.date_check = datetime.datetime.now()
        self.session.commit()
