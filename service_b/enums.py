from enum import Enum


class ServiceATaskStatus(Enum):
    """
    Перечисление статусов задачи из сервиса А
    """
    NEW = 1  # Новое
    PROCESSING = 2  # В процессе
    COMPLETED = 3  # Выполнено
    ERROR = 4  # Ошибка
