from typing import Dict, Any

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from service_b.enums import ServiceATaskStatus
from service_b.tasks import launch_task


fastapi = FastAPI()


@fastapi.post('/')
def receive_task(data: Dict[Any, Any]):
    """
    Эндпоинт API сервиса Б, получающий задачу на выполнение. В теле POST-реквеста ожидается:
        task_id: str, ID задачи
        processing_time: int, время, за которое задача будет исполнена
    """
    # запуск задачи на исполнение
    launch_task.delay(data['task_id'], int(data['processing_time']))

    # возврат информации о том, что задача была запущена
    return JSONResponse(content={'status': ServiceATaskStatus.PROCESSING.value})
