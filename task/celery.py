from celery import Celery


def make_celery():
    celery_app = Celery(__name__)
    celery_app.config_from_object('task.config')
    return celery_app


app = make_celery()
