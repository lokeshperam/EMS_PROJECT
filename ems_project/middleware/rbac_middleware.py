from django.shortcuts import redirect
from django.contrib import messages

class RBACMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'role'):
            request.role = request.user.role
            
            # Restrict admin panel access to ADMIN role only
            if request.path.startswith('/admin/') and request.user.role != 'ADMIN':
                messages.error(request, 'You do not have permission to access the admin panel.')
                return redirect('dashboard')
        
        return self.get_response(request)
