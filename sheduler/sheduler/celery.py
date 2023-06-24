from celery import Celery

from sheduler.core.config import broker_url, config


app = Celery('scheduler', include=['sheduler.tasks'])
# app.config_from_object('sheduler.celeryconfig.Settings')

# print(app.conf)

app.conf.broker_url = broker_url
app.conf.task_serializer = config.celery_config.task_serializer
app.conf.result_serializer = config.celery_config.result_serializer
app.conf.accept_content = config.celery_config.accept_content
app.conf.timezone = config.celery_config.timezone
app.conf.enable_utc = config.celery_config.enable_utc

app.conf.beat_schedule = {
    'checking_likes': {
        'task': 'sheduler.tasks.check_likes',
        'schedule': 15
    },
    'checking_comments': {
        'task': 'sheduler.tasks.check_comments',
        'schedule': 10
    }
}
