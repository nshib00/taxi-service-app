from django.contrib.auth.views import LogoutView
from django.urls import path, include

from . import views


taxi_admin_urls = [
    path('', views.AdminPageView.as_view(), name='taxi_admin'),
    path('drivers/', views.AdminDriversView.as_view(), name='admin_drivers'),
    path('drivers_search/', views.AdminDriversSearchView.as_view(), name='admin_drivers_search'),
    path('vehicles/', views.AdminVehiclesView.as_view(), name='admin_vehicles'),
    path('vehicles_search/', views.AdminVehiclesSearchView.as_view(), name='admin_vehicles_search'),
    path('shifts/', views.AdminShiftsView.as_view(), name='admin_shifts'),
    path('shifts_search/', views.AdminShiftsSearchView.as_view(), name='admin_shifts_search'),
    path('orders/', views.AdminOrdersView.as_view(), name='admin_orders'),
    path('orders_search/', views.AdminOrdersSearchView.as_view(), name='admin_orders_search'),
]

dispatcher_urls = [
    path('', views.DispatcherPageView.as_view(), name='dispatcher'),
    path('orders/', views.DispatcherOrdersView.as_view(), name='dispatcher_orders'),
    path('orders_search/', views.DispatcherOrdersSearchView.as_view(), name='dispatcher_orders_search'),
    path('free_drivers/', views.FreeDriversView.as_view(), name='dispatcher_free_drivers'),
    path('free_drivers_search/', views.FreeDriversSearchView.as_view(), name='dispatcher_free_drivers_search'),
]


driver_urls = [
    path('', views.DriverPageView.as_view(), name='driver'),
    path('shift/', views.DriverShiftManagementView.as_view(), name='driver_shift'),
    path('shift_create/', views.create_driver_shift, name='driver_shift_create'),
    path('orders/', views.DriverOrdersView.as_view(), name='driver_orders'),
    path('orders_search/', views.DriverOrdersSearchView.as_view(), name='driver_orders_search'),
]


urlpatterns = [
    path('', views.MainPageView.as_view(), name='main'),
    path('taxi_admin/', include(taxi_admin_urls)),
    path('dispatcher/', include(dispatcher_urls)),
    path('driver/', include(driver_urls)),
    path('login/', views.LoginPageView.as_view(), name='login'),
    path('logout/', views.LogoutPageView.as_view(), name='logout'),
]