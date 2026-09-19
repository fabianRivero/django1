from django.shortcuts import render 
from django.contrib.auth.decorators import login_required
from .models import Reservation

context = {
    "reservations": Reservation.objects.all(),
}

@login_required
def reservation_view(request):
    return render(request, "reservations.html", context)