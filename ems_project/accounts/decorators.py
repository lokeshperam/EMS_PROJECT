from django.http import HttpResponseForbidden

def role_required(roles):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            if request.user.role not in roles:
                return HttpResponseForbidden("Access Denied")
            return view(request, *args, **kwargs)
        return wrapper
    return decorator
