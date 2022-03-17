from typing import Dict

from django.db import models

from service_a.enums import TaskStatusEnum


class Task(models.Model):
    """
    Модель задачи
    """
    task_id = models.UUIDField('ID задачи', primary_key=True)
    name = models.CharField('Человеко-понятное название задачи', max_length=50)
    processing_time = models.PositiveIntegerField('Время выполнения в секундах')
    status = models.PositiveSmallIntegerField(
        'Статус задачи',
        choices=TaskStatusEnum.get_choices(),
        default=TaskStatusEnum.NEW,
    )

    def get_info(self) -> Dict:
        """
        Возвращает информацию о задаче в формате словаря
        """
        return {
            'task_id': str(self.task_id),
            'name': self.name,
            'processing_time': self.processing_time,
            'status': self.status,
        }

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        db_table = 'task'
