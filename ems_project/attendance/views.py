from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Attendance
from accounts.models import User

@login_required
def attendance_list(request):
    if request.user.role not in ['ADMIN', 'MANAGER']:
        messages.error(request, 'You do not have permission to view attendance.')
        return redirect('home')
    
    employee_id = request.GET.get('employee')
    month = request.GET.get('month')
    
    attendances = Attendance.objects.all()
    
    if employee_id:
        attendances = attendances.filter(employee_id=employee_id)
    
    if month:
        try:
            year, month_num = month.split('-')
            attendances = attendances.filter(date__year=int(year), date__month=int(month_num))
        except:
            pass
    
    employees = User.objects.all()
    
    context = {
        'attendances': attendances,
        'employees': employees,
        'selected_employee': employee_id,
        'selected_month': month,
    }
    return render(request, 'attendance/attendance_list.html', context)

@login_required
def my_attendance(request):
    attendances = Attendance.objects.filter(employee=request.user)
    
    today = timezone.now().date()
    first_day = today.replace(day=1)
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    month_attendances = attendances.filter(date__gte=first_day, date__lte=last_day)
    
    present_count = month_attendances.filter(status='PRESENT').count()
    absent_count = month_attendances.filter(status='ABSENT').count()
    late_count = month_attendances.filter(status='LATE').count()
    half_day_count = month_attendances.filter(status='HALF_DAY').count()
    on_leave_count = month_attendances.filter(status='ON_LEAVE').count()
    
    context = {
        'attendances': attendances[:30], 
        'present_count': present_count,
        'absent_count': absent_count,
        'late_count': late_count,
        'half_day_count': half_day_count,
        'on_leave_count': on_leave_count,
        'month_attendances': month_attendances.count(),
    }
    return render(request, 'attendance/my_attendance.html', context)

@login_required
def punch_in(request):
    today = timezone.now().date()
    existing = Attendance.objects.filter(employee=request.user, date=today).first()
    
    if existing and existing.punch_in:
        messages.warning(request, 'You are already punched in today.')
        return redirect('my_attendance')
    
    if not existing:
        existing = Attendance(employee=request.user, date=today)
    
    existing.punch_in = timezone.now()
    existing.status = 'PRESENT'
    existing.save()
    
    messages.success(request, f'Punched in at {existing.punch_in.strftime("%H:%M:%S")}')
    return redirect('my_attendance')

@login_required
def punch_out(request):
    today = timezone.now().date()
    attendance = Attendance.objects.filter(employee=request.user, date=today).first()
    
    if not attendance:
        messages.error(request, 'You need to punch in first.')
        return redirect('my_attendance')
    
    if attendance.punch_out:
        messages.warning(request, 'You are already punched out today.')
        return redirect('my_attendance')
    
    attendance.punch_out = timezone.now()
    attendance.calculate_working_hours()
    attendance.save()
    
    messages.success(request, f'Punched out at {attendance.punch_out.strftime("%H:%M:%S")}')
    return redirect('my_attendance')

@login_required
def mark_attendance(request):

    if request.user.role not in ['ADMIN', 'MANAGER']:
        messages.error(request, 'You do not have permission to mark attendance.')
        return redirect('home')
    
    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        date = request.POST.get('date')
        status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        
        employee = get_object_or_404(User, pk=employee_id)
        
        attendance, created = Attendance.objects.get_or_create(
            employee=employee,
            date=date
        )
        
        attendance.status = status
        attendance.notes = notes
        attendance.marked_by = request.user
        attendance.save()
        
        action = 'created' if created else 'updated'
        messages.success(request, f'Attendance {action} successfully.')
        return redirect('attendance_list')
    
    employees = User.objects.all()
    context = {
        'employees': employees,
        'status_choices': Attendance.STATUS_CHOICES,
    }
    return render(request, 'attendance/mark_attendance.html', context)

@login_required
def attendance_detail(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)

    if request.user != attendance.employee and request.user.role not in ['ADMIN', 'MANAGER']:
        messages.error(request, 'You do not have permission to view this record.')
        return redirect('my_attendance')
    
    context = {
        'attendance': attendance,
    }
    return render(request, 'attendance/attendance_detail.html', context)
