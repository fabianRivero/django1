#Context procesor que indica si el usuario es admin o superadmin
def admin_nav(request):

    show = False
    if request.user.is_authenticated:
        user = request.user
        if user.is_superuser:
            show = True
        else:
            profile = getattr(user, 'profile', None)
            if profile and getattr(profile, 'rol', None) == 'admin':
                show = True
    return {'show_admin_link': show}