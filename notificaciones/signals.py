from django.db.models.signals import post_save
from django.dispatch import receiver
from reservas.models import Reservation
from .tasks import create_notification, schedule_reminder

#se ejecuta despues de cada save de un Reservation
@receiver(post_save, sender=Reservation)
def on_reservation_saved(sender, instance, created, **kwargs):

    if instance.user is None:
        return
    #se evita crear muchas notificaciones si se hace un update
    ya_existe = instance.notifications.filter(kind='booking_confirmed').exists()
    if ya_existe:
        return
    #se crea la notificacion de reserva confirmada
    create_notification(
        user=instance.user,
        kind='booking_confirmed',
        title="Reserva confirmada",
        body=f"Tu reserva de {instance.service.name} para el {instance.date.strftime('%d/%m/%Y')} a las {instance.time_start.strftime('%H:%M')} está confirmada.",
        reservation=instance,
    )

    #se programa el reminder
    schedule_reminder(instance)