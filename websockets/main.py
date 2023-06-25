import asyncio
import datetime
import jwt
import websockets

from sqlalchemy import select

import config
from db import session
from logger import get_logger
from models import SendedNotification

log = get_logger(__name__)
peoples = {}


def timestamp_to_datetime(decoded: dict) -> dict:
    """Преобразуем timestamp-значения в читаемый datetime."""

    datetime_keys = ("iat", "exp")
    filtered = list(filter(lambda key: decoded.get(key) is not None, datetime_keys))
    decoded.update({key: datetime.datetime.fromtimestamp(decoded[key]) for key in filtered})
    return decoded


def auth(token):
    try:
        decoded: dict = jwt.decode(
            jwt=token,
            key=config.TokenConfiguration.secret,
            algorithms=[config.TokenConfiguration.algorithm]
        )
        decoded = timestamp_to_datetime(decoded)
        if decoded['exp'] > datetime.datetime.now():
            return decoded
        return
    except Exception as e:
        log.error(f'Ошибка авторизации: {e}')
        return


@session
def request_notifications(session, user_id: int) -> list[SendedNotification] | None:
    stmt = (
        select(SendedNotification)
        .where(SendedNotification.id_user == user_id)
        .where(SendedNotification.type_notification == 'websocket')
        .where(SendedNotification.date_check == None)
    )
    return session.scalars(stmt)


@session
def renew_notification(session, notification: SendedNotification) -> None:
    notification.date_check = datetime.datetime.now()
    session.commit()


async def send_notification(
        websocket: websockets.WebSocketServerProtocol,
        notification: SendedNotification
    ):
    await websocket.send(notification.message)


async def request_and_send_notifications(
        websocket: websockets.WebSocketServerProtocol,
        user_data: dict
    ):
    notifications = request_notifications(user_data['user_id'])
    for notification in notifications:
        await send_notification(websocket, notification)
        renew_notification(notification)


async def welcome(websocket: websockets.WebSocketServerProtocol) -> str:
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


async def receiver(websocket: websockets.WebSocketServerProtocol) -> None: 
    user_data = await welcome(websocket)
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


async def main():
    async with websockets.serve(receiver, "localhost", 8765):
        await asyncio.Future()

asyncio.run(main())
