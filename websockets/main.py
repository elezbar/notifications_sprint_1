import asyncio
import websockets

from abc import ABCMeta, abstractmethod

from db import DBhandlers
from logger import get_logger
from models import SendedNotification
from utils import auth

log = get_logger(__name__)
peoples = {}


class WebsocketHandlerABC(ABCMeta):

    @abstractmethod
    async def welcome(self, websocket: websockets.WebSocketServerProtocol) -> dict:
        """Обрабатывает новое соединение."""
        pass

    @abstractmethod
    async def receiver(self, websocket: websockets.WebSocketServerProtocol) -> None:
        """Слушает обращения пользователя."""
        pass

    @staticmethod
    @abstractmethod
    async def send_notification(
            websocket: websockets.WebSocketServerProtocol,
            notification: SendedNotification
        ) -> None:
        """Отправляет сообщение."""
        pass


class WebsocketHandler(WebsocketHandlerABC):
    
    def __init__(self):
        pass

    async def welcome(self, websocket: websockets.WebSocketServerProtocol) -> dict:
        try:
            token = await websocket.recv()
            user_data = auth(token)
            if user_data is None:
                await websocket.close(
                    websockets.frames.CloseCode.INTERNAL_ERROR,
                    'authentication failed'
                )
                return
            await websocket.send(f'Hello {user_data["username"]}!')
            await request_and_send_notifications(websocket, user_data)
            return user_data
        except Exception as e:
            log.error(f'Ошибка при приветствии пользователя: {e}')
            return

    async def receiver(self, websocket: websockets.WebSocketServerProtocol) -> None:
        user_data = await self.welcome(websocket)
        if user_data:
            peoples[user_data['user_id']] = websocket
            while True:
                message = (await websocket.recv()).strip()
                if message == 'request_notifications':
                    await request_and_send_notifications(websocket, user_data)
                    continue
        else:
            await websocket.close(
                websockets.frames.CloseCode.INTERNAL_ERROR,
                'authentication failed'
            )

    @staticmethod
    async def send_notification(
            websocket: websockets.WebSocketServerProtocol,
            notification: SendedNotification
        ) -> None:
        await websocket.send(notification.message)


async def request_and_send_notifications(
        websocket: websockets.WebSocketServerProtocol,
        user_data: dict
    ):
    db_handlers = DBhandlers()
    notifications = db_handlers.request_notifications(user_data['user_id'])
    for notification in notifications:
        await WebsocketHandler.send_notification(websocket, notification)
        db_handlers.renew_notification(notification)


async def main():
    ws_handler = WebsocketHandler()
    async with websockets.serve(ws_handler.receiver, "localhost", 8765):
        await asyncio.Future()

asyncio.run(main())
