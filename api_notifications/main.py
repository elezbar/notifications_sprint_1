
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import event, notification, send_notification, unsubscribe, wrapper
from core.config import settings
from core.logger import get_logger
from db import broker
from services.broker.rabbit_broker import RabbitBroker

logger = get_logger(__name__)

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup() -> None:
    broker.priority_brokers = {
        settings.name_instant_queues: RabbitBroker(
            settings.name_instant_queues,
            settings.broker_login,
            settings.broker_password,
            settings.broker_host,
            settings.broker_port,
        ),
        settings.name_delayed_queues: RabbitBroker(
            settings.name_delayed_queues,
            settings.broker_login,
            settings.broker_password,
            settings.broker_host,
            settings.broker_port,
        ),
    }


@app.on_event('shutdown')
async def shutdown() -> None:
    for b in broker.priority_brokers:
        b.close()


app.include_router(event.router, prefix='/api/v1/event', tags=['event'])
app.include_router(notification.router, prefix='/api/v1/notification', tags=['notification'])
app.include_router(send_notification.router, prefix='/api/v1/send_notification', tags=['send_notification'])
app.include_router(unsubscribe.router, prefix='/api/v1/unsubscribe', tags=['unsubscribe'])
app.include_router(wrapper.router, prefix='/api/v1/wrapper', tags=['wrapper'])


if __name__ == '__main__':
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)