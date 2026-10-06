from django.urls import path
from .views import notifications_view, mark_all_as_read, notifications_badge, mark_as_read

app_name = 'notificaciones'

urlpatterns = [
    path('', notifications_view, name='notifications'),
    path('marcar/<int:notification_id>/', mark_as_read, name='mark_as_read'),
    path('marcar-todas/', mark_all_as_read, name='mark_all_as_read'),
    path('badge/', notifications_badge, name='badge'),
]