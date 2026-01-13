from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from .models import Leave

@login_required
def leave_list(request):
    leaves = Leave.objects.filter(employee=request.user).order_by('-start_date')
    return render(request, 'leaves/leave_list.html', {'leaves': leaves})

@login_required
def leave_request(request):
    if request.method == "POST":
        Leave.objects.create(
            employee=request.user,
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            reason=request.POST.get('reason', ''),
            status='PENDING'
        )
        return redirect('leave_list')
    return render(request, 'leaves/leave_request.html')

@login_required
def apply_leave(request):
    if request.method == "POST":
        Leave.objects.create(
            employee=request.user,
            start_date=request.POST['start'],
            end_date=request.POST['end']
        )
    return redirect('dashboard')

@login_required
@role_required(['ADMIN', 'MANAGER'])
def pending_leaves(request):
    leaves = Leave.objects.filter(status='PENDING').order_by('-created_at')
    return render(request, 'leaves/pending_leaves.html', {'leaves': leaves})

@login_required
@role_required(['ADMIN', 'MANAGER'])
def approve_leave(request, leave_id):
   
    try:
        leave = Leave.objects.get(id=leave_id)
        leave.status = 'APPROVED'
        leave.save()
    except Leave.DoesNotExist:
        pass
    return redirect('pending_leaves')

@login_required
@role_required(['ADMIN', 'MANAGER'])
def reject_leave(request, leave_id):
  
    try:
        leave = Leave.objects.get(id=leave_id)
        leave.status = 'REJECTED'
        leave.save()
    except Leave.DoesNotExist:
        pass
    return redirect('pending_leaves')
