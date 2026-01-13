from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from accounts.models import User
from .models import Employee

@login_required
@role_required(['ADMIN', 'MANAGER'])
def employee_list(request):
    return render(request, 'employees/employee_list.html', {
        'employees': Employee.objects.all()
    })

@login_required
@role_required(['ADMIN', 'MANAGER'])
def employee_create(request):
    if request.method == "POST":
        from django.contrib.auth.hashers import make_password
        
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        
        # Create new user
        user = User.objects.create(
            username=username,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name,
            role='EMPLOYEE'
        )
        
        # Create employee record
        Employee.objects.create(
            user=user,
            designation=request.POST.get('designation', 'Employee'),
            department=request.POST.get('department', 'IT'),
            joining_date=request.POST.get('joining_date')
        )
        return redirect('employee_list')
    return render(request, 'employees/employee_form.html')

@login_required
@role_required(['ADMIN', 'MANAGER'])
def employee_detail(request, pk):
    employee = Employee.objects.get(pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee': employee})

@login_required
@role_required(['ADMIN', 'MANAGER'])
def employee_edit(request, pk):
    employee = Employee.objects.get(pk=pk)
    
    if request.method == "POST":
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        
        # Update user
        employee.user.first_name = first_name
        employee.user.last_name = last_name
        employee.user.save()
        
        # Update employee
        employee.department = request.POST.get('department', '')
        employee.designation = request.POST.get('designation', '')
        employee.joining_date = request.POST.get('joining_date')
        employee.save()
        
        return redirect('employee_detail', pk=pk)
    
    return render(request, 'employees/employee_edit.html', {'employee': employee})

@login_required
@role_required(['ADMIN', 'MANAGER'])
def employee_delete(request, pk):
    employee = Employee.objects.get(pk=pk)
    
    if request.method == "POST":
        employee.user.delete()  
        return redirect('employee_list')
    
    return render(request, 'employees/employee_delete.html', {'employee': employee})
