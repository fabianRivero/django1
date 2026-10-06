from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Reservation
from django.http import HttpResponse

from django.utils import timezone
from django.db.models import Q


@login_required
def reservation_view(request):
    now = timezone.localtime()
    user_reservations = Reservation.objects.filter(
        user=request.user
    ).filter(
        Q(date__gt=now.date()) | Q(date=now.date(), time_start__gte=now.time())
    ).order_by('date', 'time_start')
    return render(request, "reservations.html", {"reservations": user_reservations})



@login_required
def set_reservation_view(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return HttpResponse(status=404)

    if reservation.user is not None:
        return HttpResponse(status=409)

    reservation.book(request.user)
    reservation.save()
    return HttpResponse(status=200)

@login_required
def cancel_reservation_view(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return HttpResponse(status=404)

    if reservation.user_id != request.user.id:
        return HttpResponse(status=403)

    reservation.unbook()
    return HttpResponse(status=200)