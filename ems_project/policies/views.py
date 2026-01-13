from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Policy

@login_required
def policy_list(request):
    policies = Policy.objects.filter(is_active=True)
    
    # Filter by policy type if provided
    policy_type = request.GET.get('type')
    if policy_type:
        policies = policies.filter(policy_type=policy_type)
    
    context = {
        'policies': policies,
        'policy_types': Policy.POLICY_TYPES,
    }
    return render(request, 'policies/policy_list.html', context)

@login_required
def policy_detail(request, pk):
    policy = get_object_or_404(Policy, pk=pk)
    context = {
        'policy': policy,
    }
    return render(request, 'policies/policy_detail.html', context)

@login_required
def policy_create(request):
    # Check if user is admin or manager
    if request.user.role not in ['ADMIN', 'MANAGER']:
        messages.error(request, 'You do not have permission to create policies.')
        return redirect('policy_list')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        policy_type = request.POST.get('policy_type')
        content = request.POST.get('content')
        version = request.POST.get('version', '1.0')
        effective_date = request.POST.get('effective_date')
        document = request.FILES.get('document')
        
        policy = Policy.objects.create(
            title=title,
            description=description,
            policy_type=policy_type,
            content=content,
            version=version,
            effective_date=effective_date,
            document=document,
            created_by=request.user,
        )
        
        messages.success(request, 'Policy created successfully.')
        return redirect('policy_detail', pk=policy.pk)
    
    context = {
        'policy_types': Policy.POLICY_TYPES,
    }
    return render(request, 'policies/policy_create.html', context)
