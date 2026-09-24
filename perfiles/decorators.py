from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


def admin_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        user = request.user
        is_super = user.is_superuser
        is_admin_role = (
            hasattr(user, 'profile')
            and getattr(user.profile, 'rol', None) == 'admin'
        )

        if is_super or is_admin_role:
            return view_func(request, *args, **kwargs)

        return HttpResponseForbidden("No tienes permisos para acceder a esta sección.")
    return wrapper