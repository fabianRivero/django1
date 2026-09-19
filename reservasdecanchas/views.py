from django.shortcuts import render
from tipo_de_servicio.models import TypeOfService
from django.http import HttpResponseBadRequest, JsonResponse
from reservas.models import Reservation
from django.http import Http404

context = {
    "types_of_service": TypeOfService.objects.all(),
}

def home_view(request):
    return render(request, "home.html", context)

# 1. Vista que devuelve el fragmento HTML para HTMX
def open_calendar_modal(request, service_name):
    if not request.htmx:
            return HttpResponseBadRequest("Esta vista solo admite peticiones HTMX.")
    try:
         n = TypeOfService.objects.get(name = service_name)
    except TypeOfService.DoesNotExist:
         raise Http404("No hay ningun servicio registrado.")
    return render(request, "modal.html", {"service": n})

# 2. Endpoint que alimenta los eventos del calendario
def eventos_json(request):
    reservas = Reservation.objects.all()
    eventos = [
        {
            "title": reserva.service.name,
            "start": reserva.time_start.isoformat(),
            "end": reserva.time_end.isoformat() if reserva.time_end else None,
        }
        for reserva in reservas
    ]
    return JsonResponse(eventos, safe=False)