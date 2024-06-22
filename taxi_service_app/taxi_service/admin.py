from django.contrib import admin

from .models import DriverModel, VehicleModel, OrderModel, ShiftModel


@admin.register(DriverModel)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('driver_code', 'fio', 'passport', 'driver_licence', 'driver_licence_date', 'city', 'rating')
    list_display_links = ('fio',)
    ordering = ('driver_code',)
    list_per_page = 50
    search_fields = ('fio', 'city')
    exclude = ('rating',)


@admin.register(VehicleModel)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicle_code', 'reg_number', 'model', 'color', 'owner')
    list_display_links = ('reg_number',)
    ordering = ('vehicle_code',)
    list_per_page = 50
    search_fields = ('model', 'color')


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_code', 'shift_id', 'order_begin_date', 'order_end_date', 'client_phone_number', 'status')


@admin.register(ShiftModel)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('shift_code', 'driver_id', 'vehicle_id', 'shift_begin_date', 'shift_end_date')
    exclude = ('shift_end_date',)
