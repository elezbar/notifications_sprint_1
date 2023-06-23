import os
import signal
import smtplib

from dotenv import load_dotenv

from .broker.rabbit_broker import RabbitBroker
from .utils.api_request import ApiRequest
from .utils.worker import WorkerNotification

worker: WorkerNotification = None


def handler_shutdown():
    worker.stop()


if __name__ == "__main__":
    load_dotenv()
    brokers = [
        RabbitBroker(
            os.environ.get('NAME_INSTANT_QUEUE'),
            os.environ.get('BROKER_LOGIN'),
            os.environ.get('BROKER_PASSWORD'),
            os.environ.get('BROKER_HOST'),
            int(os.environ.get('BROKER_PORT')),
        ),
        RabbitBroker(
            os.environ.get('NAME_DELAYED_QUEUE'),
            os.environ.get('BROKER_LOGIN'),
            os.environ.get('BROKER_PASSWORD'),
            os.environ.get('BROKER_HOST'),
            int(os.environ.get('BROKER_PORT')),
        ),
    ]
    smtp_server = smtplib.SMTP_SSL(
        os.environ.get('SMTP_HOST'),
        int(os.environ.get('SMTP_PORT'))
    )
    smtp_server.login(
        os.environ.get('SMTP_LOGIN'),
        os.environ.get('SMTP_PASSWORD')
    )
    api_request = ApiRequest(
        os.environ.get('ACCESS_TOKEN'),
    )

    worker = WorkerNotification(
        brokers,
        smtp_server,
        api_request,
        os.environ.get('URL_GET_USER'),
        os.environ.get('EMAIL_FROM')
    )

    signal.signal(signal.SIGINT, handler_shutdown)
    signal.signal(signal.SIGTERM, handler_shutdown)
    worker.run()
