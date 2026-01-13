from django.urls import path
from .views import leave_list, leave_request, apply_leave, pending_leaves, approve_leave, reject_leave

urlpatterns = [
    path('', leave_list, name='leave_list'),
    path('request/', leave_request, name='leave_request'),
    path('apply/', apply_leave, name='apply_leave'),
    path('pending/', pending_leaves, name='pending_leaves'),
    path('<int:leave_id>/approve/', approve_leave, name='approve_leave'),
    path('<int:leave_id>/reject/', reject_leave, name='reject_leave'),
]