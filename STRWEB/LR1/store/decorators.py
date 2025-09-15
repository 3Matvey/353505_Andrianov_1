from django.core.exceptions import PermissionDenied

def employee_required(view_func):
    def _wrapped(request, *args, **kwargs):
        user = request.user
        if not (user.is_superuser or hasattr(user, 'employee_profile')):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped
