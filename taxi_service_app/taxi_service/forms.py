from django import forms

from .models import OrderModel, ShiftModel, DriverModel, VehicleModel


class AddShiftForm(forms.ModelForm):
    vehicle_id = forms.ModelChoiceField(queryset=VehicleModel.objects.all())
    driver_id = forms.ModelChoiceField(queryset=DriverModel.objects.all())

    class Meta:
        model = ShiftModel
        fields = ['driver_id', 'vehicle_id']


class OrderSearchForm(forms.ModelForm):
    status = forms.ModelChoiceField(
        queryset=OrderModel.objects.values_list('status', flat=True).distinct(),
        required=False
    )

    class Meta:
        model = OrderModel
        fields = ['status']


class BaseDriverSearchForm(forms.ModelForm):
    class Meta:
        model = DriverModel
        fields = ['fio', 'city']


class FreeDriversSearchForm(BaseDriverSearchForm):
    pass


class AdminDriversSearchForm(BaseDriverSearchForm):
    pass


class AdminVehiclesSearchForm(forms.ModelForm):
    class Meta:
        model = VehicleModel
        fields = ['reg_number']
