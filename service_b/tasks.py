from time import sleep

from service_b.consts import TIME_TO_MAKE_ERROR
from service_b.enums import ServiceATaskStatus
from service_b.gateway import send_change_status
from service_b.worker import service_b_celery


@service_b_celery.task(name='launch_task')
def launch_task(task_id: str, processing_time: int):
    """
    Celery-таска, запускающая на исполнение задачу, пришедшую из сервиса А.
    """
    # имитация работы над задачей
    sleep(processing_time)

    # задача выполнена - определяется ее статус
    # если ожидалось исполнение за 13 секунд, то считается, что задача выполнена с ошибкой
    new_status = (
        ServiceATaskStatus.ERROR.value
        if processing_time == TIME_TO_MAKE_ERROR
        else ServiceATaskStatus.COMPLETED.value
    )
    # отправка нового статуса в сервис А для обновления
    send_change_status(task_id, new_status)
