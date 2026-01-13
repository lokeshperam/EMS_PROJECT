from django.urls import path
from .views import employee_list, employee_create, employee_detail, employee_edit, employee_delete

urlpatterns = [
    path('', employee_list, name='employee_list'),
    path('create/', employee_create, name='employee_create'),
    path('<int:pk>/view/', employee_detail, name='employee_detail'),
    path('<int:pk>/edit/', employee_edit, name='employee_edit'),
    path('<int:pk>/delete/', employee_delete, name='employee_delete'),
]