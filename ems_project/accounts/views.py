from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from employees.models import Employee
from leaves.models import Leave
from tasks.models import Task
from issues.models import Issue

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    """Main dashboard with statistics"""
    context = {
        'total_employees': Employee.objects.count(),
        'pending_leaves': Leave.objects.filter(status='PENDING').count(),
        'active_tasks': Task.objects.filter(status='IN_PROGRESS').count(),
        'open_issues': Issue.objects.filter(status='OPEN').count(),
    }
    return render(request, 'dashboard/admin_dashboard.html', context)
