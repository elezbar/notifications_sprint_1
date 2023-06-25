import datetime
import jwt

from config import config
from logger import get_logger

log = get_logger(__name__)


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
            key=config.token.secret,
            algorithms=[config.token.algorithm]
        )
        decoded = timestamp_to_datetime(decoded)
        if decoded['exp'] > datetime.datetime.now():
            return decoded
        return
    except Exception as e:
        log.error(f'Ошибка авторизации: {e}')
        return
