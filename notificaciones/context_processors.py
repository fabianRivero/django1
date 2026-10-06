#context procesor que calcula el numero de notificaciones no leidas
#se usa para que el numero de notificaciones aparezca en el navbar sin necesidad de hacer refresh
def notifications_context(request):
    unread_count = 0
    if request.user.is_authenticated:
        from .models import Notification
        unread_count = request.user.notifications.filter(read=False).count()
    return {'unread_count': unread_count}