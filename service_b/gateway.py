import os

import requests
from service_b import settings


def send_change_status(task_id: str, status: int):
    """
    Функция, отправляющая POST-запрос в сервис А о том, что у задачи с task_id нужно поменять статус на новый
    """
    headers = {}
    if os.environ.get('RUNNING_IN_CONTAINER'):
        headers.update({'HTTP_HOST': '0.0.0.0:8000'})

    requests.post(
        url=f'{settings.SERVICE_A_URL}api/change-status/',
        json={'task_id': task_id, 'status': status},
        headers=headers,
    )
