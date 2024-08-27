from celery import Celery
from .config import Config
from celery.schedules import crontab

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=Config.result_backend,
        broker=Config.broker_url
    )
    celery.conf.update(app.config)

    celery.conf.beat_schedule = {
        'send-emails-every-minute': {
            'task': 'send_emails_task',
            'schedule': crontab(minute='*'),
        },
    }

    return celery
