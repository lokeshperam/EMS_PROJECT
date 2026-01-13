from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from accounts.models import User
from employees.models import Employee
from .models import Task

@login_required
def task_list(request):
   
    if request.user.is_superuser or request.user.role in ['ADMIN', 'MANAGER']:
        tasks = Task.objects.all().order_by('-created_at')
    else:
        tasks = Task.objects.filter(assigned_to=request.user).order_by('-created_at')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
@role_required(['ADMIN', 'MANAGER'])
def task_create(request):
   
    if request.method == "POST":
        employee_id = request.POST.get('assigned_to')
        try:
            assigned_to = User.objects.get(id=employee_id)
            Task.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description', ''),
                assigned_to=assigned_to,
                assigned_by=request.user,
                status='PENDING'
            )
            return redirect('task_list')
        except User.DoesNotExist:
            pass
    

    employees = User.objects.filter(employee__isnull=False)
    context = {'employees': employees}
    return render(request, 'tasks/task_create.html', context)

@login_required
def my_tasks(request):
    return render(request, 'tasks/task_list.html', {
        'tasks': Task.objects.filter(assigned_to=request.user)
    })

@login_required
def task_detail(request, pk):
    task = Task.objects.get(pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
@role_required(['ADMIN', 'MANAGER'])
def task_edit(request, pk):
    task = Task.objects.get(pk=pk)
    
    if request.method == "POST":
        employee_id = request.POST.get('assigned_to')
        try:
            assigned_to = User.objects.get(id=employee_id)
            task.title = request.POST.get('title')
            task.description = request.POST.get('description', '')
            task.assigned_to = assigned_to
            task.status = request.POST.get('status', 'PENDING')
            task.save()
            return redirect('task_detail', pk=pk)
        except User.DoesNotExist:
            pass
    
    employees = User.objects.filter(employee__isnull=False)
    return render(request, 'tasks/task_edit.html', {'task': task, 'employees': employees})

@login_required
@role_required(['ADMIN', 'MANAGER'])
def task_delete(request, pk):
    task = Task.objects.get(pk=pk)
    
    if request.method == "POST":
        task.delete()
        return redirect('task_list')
    
    return render(request, 'tasks/task_delete.html', {'task': task})

@login_required
def task_update_status(request, pk):
    task = Task.objects.get(pk=pk)
    
    # Only allow assigned employee to update status
    if task.assigned_to != request.user:
        return redirect('task_list')
    
    if request.method == "POST":
        task.status = request.POST.get('status')
        task.save()
        return redirect('task_detail', pk=pk)
    
    return render(request, 'tasks/task_update_status.html', {'task': task})
