from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class DriverLoginRequiredMixin(LoginRequiredMixin):
    redirect_field_name = 'driver'


class AdminLoginRequiredMixin(LoginRequiredMixin):
    redirect_field_name = 'taxi_admin'


class DispatcherLoginRequiredMixin(LoginRequiredMixin):
    redirect_field_name = 'dispatcher'


class DriverPermissionRequiredMixin(PermissionRequiredMixin):
    permission_required = [
        'taxi_service.view_order_model',
        'taxi_service.view_vehicle_model',
        'taxi_service.add_shift_model',
        'taxi_service.change_shift_model',
        'taxi_service.view_shift_model',
    ]


class DispatcherPermissionRequiredMixin(PermissionRequiredMixin):
    permission_required = [
        'taxi_service.view_driver_model',
        'taxi_service.add_order_model',
        'taxi_service.view_order_model',
    ]


class AdminPermissionRequiredMixin(PermissionRequiredMixin):
    permission_required = [
        'taxi_service.add_driver_model',
        'taxi_service.change_driver_model',
        'taxi_service.delete_driver_model',
        'taxi_service.view_driver_model',
        'taxi_service.add_vehicle_model',
        'taxi_service.change_vehicle_model',
        'taxi_service.delete_vehicle_model',
        'taxi_service.view_vehicle_model',
        'taxi_service.view_order_model',
        'taxi_service.view_shift_model',
        'taxi_service.add_user',
        'taxi_service.change_user',
        'taxi_service.delete_user',
        'taxi_service.view_user',
    ]


# class DriverAccessMixin(UserPassesTestMixin):
#     def test_func(self):
#         return self.request.user.email.endswith('@example.com')