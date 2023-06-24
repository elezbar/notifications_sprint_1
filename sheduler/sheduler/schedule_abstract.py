from abc import ABCMeta, abstractmethod
from sheduler.models.models import Notification


class NotificationsABC(metaclass=ABCMeta):

    @abstractmethod
    def get_notifications_from_db(self, session, event_id: int, event_name: str) -> None:
        """Планово берёт из базы все уведомления, которые необходимо отслеживать."""
        pass
    
    @abstractmethod
    def iterate_notifications(self, notifications: list) -> None:
        """Перебирает все уведомления, и ставит задачи на проверку."""
        pass
      
    @abstractmethod
    def check_update_task(self, notification: Notification) -> None:
        """Осуществляет проверку уведомления в таске."""
        pass
    
    @abstractmethod
    def update_notifications_in_db(self, session, notification: Notification, result: dict) -> None:
        """Обновляет уведомление в БД."""
        pass
    
    @abstractmethod
    def send_upadte_to_api(self, notification: Notification, result: dict) -> None:
        """Отправляет уведомление в API сервис."""
        pass
