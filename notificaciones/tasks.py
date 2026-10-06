from datetime import timedelta
from django.utils import timezone
from django_q.tasks import schedule
from .models import Notification

def create_notification(user, kind, title, body, reservation=None):
    Notification.objects.create(
        user=user,
        kind=kind,
        title=title,
        body=body,
        reservation=reservation,
    )


#se programa el envio del reminder 1 hora antes de la reserva
def schedule_reminder(reservation):
    fecha_hora_inicio = timezone.make_aware(
        timezone.datetime.combine(reservation.date, reservation.time_start)
    )
    ejecutar_en = fecha_hora_inicio - timedelta(hours=1)

    #solo si la fecha no paso ya
    if ejecutar_en <= timezone.now():
        return

    schedule(
        'notificaciones.tasks.send_reminder',  # 1. Función a ejecutar
        args=(reservation.id,),               # 2. Argumentos que recibirá
        schedule_type='O',                    # 3. Tipo de frecuencia (una sola vez)
        next_run=ejecutar_en,                 # 4. Momento exacto de ejecución
    )

#funcion que se ejecuta cuando es tiempo de enviar el reminder
def send_reminder(reservation_id):
    from reservas.models import Reservation

    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return

    if reservation.user is None:
        return

    create_notification(
        user=reservation.user,
        kind='reminder',
        title=f"Recordatorio: tu reserva empieza en una hora.",
        body=f"Tu reserva de {reservation.service.name} es hoy a las {reservation.time_start.strftime('%H:%M')}",
        reservation=reservation,
    )