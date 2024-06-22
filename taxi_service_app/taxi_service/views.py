from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView

from .forms import OrderSearchForm, FreeDriversSearchForm, AdminDriversSearchForm, AdminVehiclesSearchForm, AddShiftForm
from .mixins import DriverLoginRequiredMixin, DispatcherLoginRequiredMixin, AdminLoginRequiredMixin
from .models import OrderModel, DriverModel, VehicleModel, ShiftModel


class MainPageView(TemplateView):
    template_name = 'templates/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'TaxiService'
        return context


class DriverPageView(DriverLoginRequiredMixin, TemplateView):
    template_name = 'templates/driver/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'TaxiService | Меню водителя'
        context['header_text'] = 'Меню водителя'
        context['back_btn_url'] = 'driver'
        return context


class DriverShiftManagementView(DriverLoginRequiredMixin, TemplateView):
    template_name = 'templates/driver/shift.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_text'] = 'Управление сменой'
        context['form'] = AddShiftForm
        return context


# class DriverShiftCreateView(DriverLoginRequiredMixin, CreateView):
#     model = ShiftModel
#     template_name = 'templates/driver/shift_create.html'
#     success_url = reverse_lazy('shift')
#     form_class = AddShiftForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['header_text'] = 'Создать смену'
#         return context

def create_driver_shift(request):
    if request.method == 'POST':
        form = AddShiftForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('driver')
    else:
        form = AddShiftForm()
    context = {
        'header_text': 'Открыть смену',
        'form': form
    }
    return render(request, 'templates/driver/shift_create.html', context)


class DriverOrdersView(DriverLoginRequiredMixin, ListView):
    template_name = 'templates/driver/orders.html'
    model = OrderModel
    context_object_name = 'orders'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_text'] = 'Список заказов водителя'
        context['form'] = OrderSearchForm()
        return context



class DriverOrdersSearchView(DriverOrdersView, DriverLoginRequiredMixin):
    model = None

    def get_queryset(self):
        if not self.request.GET.get('status'):
            return OrderModel.objects.order_by('order_code')
        return OrderModel.objects.filter(status=self.request.GET.get('status')).order_by('order_code')

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class DispatcherPageView(DispatcherLoginRequiredMixin, TemplateView):
    template_name = 'templates/dispatcher/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'TaxiService | Меню диспетчера'
        context['header_text'] = 'Меню диспетчера'
        context['back_btn_url'] = 'dispatcher'
        return context


class DispatcherOrdersView(DispatcherLoginRequiredMixin, ListView):
    template_name = 'templates/dispatcher/orders.html'
    model = OrderModel
    context_object_name = 'orders'

    def get_queryset(self):
        if not self.request.GET.get('status'):
            return OrderModel.objects.order_by('order_code')
        return OrderModel.objects.filter(status=self.request.GET.get('status')).order_by('order_code')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_text'] = 'Список заказов'
        context['form'] = OrderSearchForm()
        return context


class DispatcherOrdersSearchView(DispatcherOrdersView, DispatcherLoginRequiredMixin):
    model = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_text'] = 'Список заказов'
        # context['form'] = OrderSearchForm()
        return context


class FreeDriversView(DispatcherLoginRequiredMixin, ListView):
    template_name = 'templates/dispatcher/free_drivers.html'
    model = ShiftModel
    context_object_name = 'shifts'

    def get_queryset(self):
        return ShiftModel.objects.filter(shift_end_date__isnull=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_text'] = 'Список свободных водителей'
        context['drivers_count'] = ShiftModel.objects.filter(shift_end_date__isnull=True).count()
        return context


class FreeDriversSearchView(FreeDriversView, DispatcherLoginRequiredMixin):
    model = None

    def get_queryset(self):
        return ShiftModel.objects.filter(
            Q(shift_end_date__isnull=True) &
            Q(driver_id__fio__istartswith=self.request.GET.get('name')) &
            Q(driver_id__city__istartswith=self.request.GET.get('city'))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FreeDriversSearchForm()
        context['drivers_count'] = ShiftModel.objects.filter(
            Q(shift_end_date__isnull=True) &
            Q(driver_id__fio__istartswith=self.request.GET.get('name')) &
            Q(driver_id__city__istartswith=self.request.GET.get('city'))
        ).count()
        return context


class AdminPageView(AdminLoginRequiredMixin, TemplateView):
    template_name = 'templates/taxi_admin/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'TaxiService | Меню администратора'
        context['header_text'] = 'Меню администратора'
        context['back_btn_url'] = 'taxi_admin'
        return context


class AdminDriversView(AdminLoginRequiredMixin, ListView):
    template_name = 'templates/taxi_admin/drivers.html'
    model = DriverModel
    context_object_name = 'drivers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_text'] = 'Справочник водителей'
        context['drivers_count'] = DriverModel.objects.count()
        return context


class AdminDriversSearchView(AdminDriversView, AdminLoginRequiredMixin):
    model = None

    def get_queryset(self):
        return DriverModel.objects.filter(
            Q(fio__istartswith=self.request.GET.get('name')) &
            Q(city__istartswith=self.request.GET.get('city'))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AdminDriversSearchForm()
        context['drivers_count'] = DriverModel.objects.filter(
            Q(fio__istartswith=self.request.GET.get('name')) &
            Q(city__istartswith=self.request.GET.get('city'))
        ).count()
        return context


class AdminShiftsView(AdminLoginRequiredMixin, ListView):
    template_name = 'templates/taxi_admin/shifts.html'
    model = ShiftModel
    context_object_name = 'shifts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_text'] = 'Справочник смен'
        context['shifts_count'] = ShiftModel.objects.count()
        return context


class AdminShiftsSearchView(AdminShiftsView, AdminLoginRequiredMixin):
    model = None

    def get_queryset(self):
        return ShiftModel.objects.filter(
            Q(driver_id__fio__istartswith=self.request.GET.get('driver_name')) &
            Q(driver_id__city__istartswith=self.request.GET.get('city'))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_text'] = 'Справочник смен'
        context['shifts_count'] = ShiftModel.objects.filter(
            Q(driver_id__fio__istartswith=self.request.GET.get('driver_name')) &
            Q(driver_id__city__istartswith=self.request.GET.get('city'))
        ).count()
        return context


class AdminVehiclesView(AdminLoginRequiredMixin, ListView):
    template_name = 'templates/taxi_admin/vehicles.html'
    model = VehicleModel
    context_object_name = 'vehicles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_text'] = 'Справочник транспортных средств'
        context['vehicles_count'] = VehicleModel.objects.count()
        return context


class AdminVehiclesSearchView(AdminVehiclesView, AdminLoginRequiredMixin):
    model = None

    def get_queryset(self):
        return VehicleModel.objects.filter(
            reg_number__startswith=self.request.GET.get('reg_number')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AdminVehiclesSearchForm()
        context['vehicles_count'] = VehicleModel.objects.filter(
            reg_number__startswith=self.request.GET.get('reg_number')
        ).count()
        return context


class AdminOrdersView(AdminLoginRequiredMixin, ListView):
    template_name = 'templates/taxi_admin/orders.html'
    model = OrderModel
    context_object_name = 'orders'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_text'] = 'Справочник заказов'
        context['orders_count'] = OrderModel.objects.count()
        return context


class AdminOrdersSearchView(AdminOrdersView, AdminLoginRequiredMixin):
    model = None

    def get_queryset(self):
        return OrderModel.objects.filter(
            Q(shift_id__driver_id__fio__istartswith=self.request.GET.get('driver_name')) &
            Q(shift_id__driver_id__city__istartswith=self.request.GET.get('city'))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FreeDriversSearchForm()
        context['orders_count'] = OrderModel.objects.filter(
            Q(shift_id__driver_id__fio__istartswith=self.request.GET.get('driver_name')) &
            Q(shift_id__driver_id__city__istartswith=self.request.GET.get('city'))
        ).count()
        return context


class LoginPageView(LoginView):
    form_class = AuthenticationForm
    template_name = 'templates/login.html'
    extra_context = {'title': 'TaxiService | Авторизация'}

    def get_success_url(self):
        if self.request.user.username.startswith('driver'):
            return reverse_lazy('driver')
        if self.request.user.username.startswith('dispatcher'):
            return reverse_lazy('dispatcher')
        if self.request.user.username.startswith('taxiadmin') or self.request.user.username == 'admin':
            return reverse_lazy('taxi_admin')


class LogoutPageView(LogoutView):
    extra_context = {'title': 'TaxiService | Выход из системы'}

    def get_success_url(self):
        return reverse_lazy('main')

