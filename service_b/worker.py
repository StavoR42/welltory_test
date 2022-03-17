import os

from celery import Celery


service_b_celery = Celery('service_b')

host = 'redis' if os.environ.get('RUNNING_IN_CONTAINER') else 'localhost'
service_b_celery.conf.broker_url = f'redis://{host}:6379/0'
service_b_celery.conf.result_backend = f'redis://{host}:6379/0'

service_b_celery.autodiscover_tasks(['service_b'])
