from django.db import models


class OrderStatusChoices(models.TextChoices):
    ACCEPTED = 'Принят'
    IN_PROGRESS = 'Выполняется'
    DONE = 'Завершен'
    CANCELLED = 'Отменен'


class OrderMarkChoices(models.IntegerChoices):
    NO_MARK = (0, 'Без оценки')
    ONE = (1, '1')
    TWO = (2, '2')
    THREE = (3, '3')
    FOUR = (4, '4')
    FIVE = (5, '5')
