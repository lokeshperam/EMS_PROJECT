from django.contrib import admin
from django.urls import path, include
from accounts.views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('employees/', include('employees.urls')),
    path('leaves/', include('leaves.urls')),
    path('tasks/', include('tasks.urls')),
    path('policies/', include('policies.urls')),
    path('attendance/', include('attendance.urls')),
]
