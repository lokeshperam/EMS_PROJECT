from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_list, name='attendance_list'),
    path('my/', views.my_attendance, name='my_attendance'),
    path('punch-in/', views.punch_in, name='punch_in'),
    path('punch-out/', views.punch_out, name='punch_out'),
    path('mark/', views.mark_attendance, name='mark_attendance'),
    path('<int:pk>/', views.attendance_detail, name='attendance_detail'),
]
