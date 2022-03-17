import json
from uuid import UUID, uuid4

import requests
from django.conf import settings
from django.http import JsonResponse

from service_a.enums import TaskStatusEnum
from service_a.models import Task


def tasks(request):
    """
    Вьюха, отображающая все имеющиеся в БД задачи, если пришел реквест метода GET; либо отсылающая задачу в сервис Б,
    если пришел реквест метода POST. Для корректной отправки задачи в сервис Б нужно иметь в теле реквеста параметры
        name: str, человеко-читаемое название задачи
        processing_time: int, кол-во секунд, которое выполняется задача
    """
    if request.method == 'GET':
        # возврат инфо по всем задачам
        tasks_ = Task.objects.all()
        result = [task.get_info() for task in tasks_]

    elif request.method == 'POST':
        # сохранение параметров задачи и ее запуск
        name = request.POST.get('name')
        processing_time = request.POST.get('processing_time')

        # базовая валидация на существование параметров
        if not name or not processing_time:
            result = {'error': 'Missing required parameters - \'name\' or \'processing_time\''}

        else:
            # сохранение нового объекта задачи
            new_task = Task(
                pk=uuid4(),
                name=name,
                processing_time=int(processing_time),
            )
            new_task.save()

            task_id = str(new_task.pk)

            # отправка запроса в сервис Б для запуска задачи на исполнение
            response = requests.post(
                url=settings.SERVICE_B_URL,
                json={
                    'task_id': task_id,
                    'processing_time': processing_time,
                },
            )
            # ожидается, что сервис вернет ответ со статусом "В процессе"
            if response.status_code == 200:
                new_status = response.json().get('status')
                # любой другой статус означает ошибку
                new_status = new_status if new_status in TaskStatusEnum.values else TaskStatusEnum.ERROR

                new_task.status = new_status
                new_task.save()

            # возвращается ID новой задачи, которая уже отдана на обработку
            result = {'task_id': task_id}

    else:
        # базовая валидация на метод реквеста
        result = {'error': 'Wrong request method'}

    return JsonResponse(result, safe=False)


def view_one_task(request, task_id):
    """
    Вьюха, которая отображает задачу по ее ID
    """
    if request.method == 'GET':
        try:
            task = Task.objects.get(pk=UUID(task_id))
        except Task.DoesNotExist:
            result = {'error': f'Task with id {task_id} does not exist'}
        except ValueError:
            result = {'error': 'Wrong UUID'}
        else:
            result = task.get_info()

        return JsonResponse(result)


def change_status(request):
    """
    Вьюха, которая изменяет статус существующей задачи по ID. В теле POST-реквеста должны быть:
        status: int, новый статус для задачи
        task_id: str, ID задачи для обновления
    """
    if request.method == 'POST':
        # совместимость с разными типами Content-Type
        post = request.POST or json.loads(request.body)

        new_status = post.get('status')
        new_status = new_status if new_status in TaskStatusEnum.values else TaskStatusEnum.ERROR

        task_id = post.get('task_id')
        task = Task.objects.filter(pk=UUID(task_id)).first()

        if task:
            # обновление статуса
            task.status = new_status
            task.save()

        return JsonResponse({'status': 'success'})
