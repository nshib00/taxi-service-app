from django.db import models
from django.db.models import Sum

from . import choices


class DriverModel(models.Model):
    driver_code = models.BigAutoField(primary_key=True, verbose_name='Код водителя')
    fio = models.CharField(max_length=60, verbose_name='ФИО водителя')
    passport = models.CharField(max_length=10, unique=True, verbose_name='Паспорт')
    driver_licence = models.CharField(max_length=10, unique=True, verbose_name='Водит. удост.')
    driver_licence_date = models.DateField(verbose_name='Дата выдачи ВУ')
    city = models.CharField(max_length=30, verbose_name='Город')
    rating = models.FloatField(default=0, verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Водители'
        verbose_name_plural = 'Водители'
        constraints = (
            models.CheckConstraint(
                check=models.Q(rating__gte=0) & models.Q(rating__lte=5),
                name='driver_rating_gte_0_lte_5'
            ),
        )


class VehicleModel(models.Model):
    vehicle_code = models.BigAutoField(primary_key=True, verbose_name='Код трансп. ср-ва')
    model = models.CharField(max_length=50, verbose_name='Марка ТС')
    color = models.CharField(max_length=20, verbose_name='Цвет')
    reg_number = models.CharField(max_length=15, unique=True, verbose_name='Рег. номер')
    owner = models.CharField(max_length=60, verbose_name='Собственник ТС')

    class Meta:
        verbose_name = 'Транспортные средства'
        verbose_name_plural = 'Транспортные средства'


class ShiftModel(models.Model):
    shift_code = models.BigAutoField(primary_key=True)
    driver_id = models.ForeignKey(DriverModel, on_delete=models.CASCADE)
    vehicle_id = models.ForeignKey(VehicleModel, on_delete=models.CASCADE)
    shift_begin_date = models.DateTimeField(auto_now_add=True)
    shift_end_date = models.DateTimeField(null=True)

    class Meta:
        verbose_name = 'Смены'
        verbose_name_plural = 'Смены'

    @property
    def orders_count(self):
        return OrderModel.objects.filter(shift_id=self.shift_code).count()

    @property
    def total_orders_cost(self):
        return OrderModel.objects.select_related('shift_id').aggregate(Sum('cost', default=0))['cost__sum']
            # .filter(shift_id=self.shift_code).values_list('cost', flat=True)


class OrderModel(models.Model):
    order_code = models.BigAutoField(primary_key=True)
    shift_id = models.ForeignKey(ShiftModel, on_delete=models.CASCADE)
    order_begin_date = models.DateTimeField()
    order_end_date = models.DateTimeField()
    client_phone_number = models.CharField(max_length=12)
    status = models.CharField(
        max_length=50, choices=choices.OrderStatusChoices
    )
    mark = models.PositiveSmallIntegerField(choices=choices.OrderMarkChoices, default=0)
    cost = models.FloatField()
    boarding_address = models.CharField(max_length=100)
    destination_address = models.CharField(max_length=100)

    class Meta:
        constraints = (
            models.CheckConstraint(
                check=models.Q(cost__gt=0),
                name='order_cost_gt_0'
            ),
        )
        verbose_name = 'Заказы'
        verbose_name_plural = 'Заказы'
