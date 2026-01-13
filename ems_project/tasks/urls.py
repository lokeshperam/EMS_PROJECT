from django.urls import path
from .views import task_list, task_create, my_tasks, task_detail, task_edit, task_delete, task_update_status

urlpatterns = [
    path('', task_list, name='task_list'),
    path('create/', task_create, name='task_create'),
    path('my-tasks/', my_tasks, name='tasks'),
    path('<int:pk>/view/', task_detail, name='task_detail'),
    path('<int:pk>/edit/', task_edit, name='task_edit'),
    path('<int:pk>/delete/', task_delete, name='task_delete'),
    path('<int:pk>/update-status/', task_update_status, name='task_update_status'),
]