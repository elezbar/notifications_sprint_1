import os
import signal
import smtplib

from dotenv import load_dotenv

from .broker.rabbit_broker import RabbitBroker
from .config import config
from .utils.api_request import ApiRequest
from .utils.worker import WorkerNotification

worker: WorkerNotification = None


def handler_shutdown():
    worker.stop()


if __name__ == "__main__":
    brokers = [
        RabbitBroker(
            config.broker.name_instant_queue,
            config.broker.broker_login,
            config.broker.broker_password,
            config.broker.broker_host,
            config.broker.broker_port
        ),
        RabbitBroker(
            config.broker.name_delayed_queue,
            config.broker.broker_login,
            config.broker.broker_password,
            config.broker.broker_host,
            config.broker.broker_port
        )
    ]
    smtp_server = smtplib.SMTP_SSL(
        config.smtp.smtp_host,
        config.smtp.smtp_port
    )
    smtp_server.login(
        config.smtp.smtp_login,
        config.smtp.smtp_password
    )
    api_request = ApiRequest(
        config.broker.access_token,
    )
    worker = WorkerNotification(
        brokers,
        smtp_server,
        api_request,
        config.constants.url_get_user,
        config.constants.email_from
    )

    signal.signal(signal.SIGINT, handler_shutdown)
    signal.signal(signal.SIGTERM, handler_shutdown)
    worker.run()
