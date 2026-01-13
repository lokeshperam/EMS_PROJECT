from django.urls import path
from . import views

urlpatterns = [
    path('', views.policy_list, name='policy_list'),
    path('create/', views.policy_create, name='policy_create'),
    path('<int:pk>/', views.policy_detail, name='policy_detail'),
]
