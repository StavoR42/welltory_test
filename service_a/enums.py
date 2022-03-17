from typing import Tuple, Any


"""
Базовые компоненты
"""


class BaseEnumerate:
    """
    Базовый класс для внутренних перечислений.

    Содержит общий для всех перечислений метод get_choices, позволяющий задать выбор в поле для модели.
    """
    values = {}

    @classmethod
    def get_choices(cls) -> Tuple[Tuple[Any, Any]]:
        """
        Возвращает текущее перечисление с его кастомными значениями в формате
        ((enum_item1, enum_val1), (enum_item2, enum_val2), ...)
        """
        return tuple((item, value) for item, value in cls.values.items())


"""
Перечисления
"""


class TaskStatusEnum(BaseEnumerate):
    """
    Перечисление статусов для задачи
    """
    NEW = 1
    PROCESSING = 2
    COMPLETED = 3
    ERROR = 4

    values = {
        NEW: 'Новое',
        PROCESSING: 'В процессе',
        COMPLETED: 'Выполнено',
        ERROR: 'Ошибка',
    }
