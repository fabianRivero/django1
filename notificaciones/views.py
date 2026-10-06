from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notifications_view(request):
    notifications = request.user.notifications.all()[:50]
    unread_count = request.user.notifications.filter(read=False).count()
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'notifications.html', context)


@login_required
def mark_as_read(request, notification_id):
    try:
        notification = Notification.objects.get(
            id=notification_id,
            user=request.user,
        )
        notification.read = True
        notification.save()
    except Notification.DoesNotExist:
        pass
    return redirect('notificaciones:notifications')


@login_required
def mark_all_as_read(request):
    if request.method == 'POST':
        request.user.notifications.filter(read=False).update(read=True)
    return redirect('notificaciones:notifications')


@login_required
# renderizado del html del badge de notificaciones sin leer
def notifications_badge(request):
    unread_count = request.user.notifications.filter(read=False).count()
    return render(request, 'badge.html', {'unread_count': unread_count})