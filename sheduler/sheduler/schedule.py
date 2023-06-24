
import asyncio

from datetime import datetime, timedelta
from sqlalchemy import select

from sheduler.core import utils
from sheduler.core.config import config
from sheduler.models.models import Notification
from sheduler.postgres.db import session
from sheduler.schedule_abstract import NotificationsABC


class Notifications(NotificationsABC):

    @session
    def __init__(self, event_id: int, event_name: str, session):
        self.session = session
        self.event_id = event_id
        self.event_name = event_name

    def get_notifications_from_db(self) -> None:
        toDate = datetime.now() - timedelta(days=14)
        stmt = (
            select(Notification)
            .where(Notification.id_event == self.event_id)
            .where(Notification.last_update > toDate).limit(50)
        )
        self.iterate_notifications(self.session.scalars(stmt))
    
    def iterate_notifications(self, notifications: Notification) -> None:
        """Перебирает все уведомления, и ставит задачи на проверку."""
        for notification in notifications:
            self.check_update_task(notification)

    def check_update_task(self, notification: Notification) -> None:
        """Осуществляет проверку уведомления в таске."""
        url = f'{config.constants.ugs_url}{self.event_name}/{notification.id_content}'
        result = asyncio.run(utils.request_get('https://catfact.ninja/fact'))
        if result:
            # if len(result['likes']):
            if result['length']:
                self.send_upadte_to_api(notification, result)
        
    
    def update_notifications_in_db(self, session, notification: Notification, result: dict) -> None:
        """Обновляет уведомление в БД."""
        # notification.last_update = result['last_date']
        notification.last_update = datetime.now() + timedelta(hours=1)
        session.commit()
    
    def send_upadte_to_api(self, notification: Notification, result: dict) -> None:
        """Отправляет уведомление в API сервис."""
        result = asyncio.run(utils.request_post(config.constants.notifications_url, result))
        if result:
            if result['result'] == 'ok':
                self.update_notifications_in_db(notification, result)
