from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Reservation
from django.http import HttpResponse

context = {}

@login_required
def reservation_view(request):
    user_reservations = Reservation.objects.filter(user = request.user)
    context.update({"reservations": user_reservations})
    return render(request, "reservations.html", context)


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