from django.shortcuts import render, redirect
from tipo_de_servicio.models import TypeOfService
from django.http import HttpResponseBadRequest, JsonResponse
from reservas.models import Reservation
from django.http import Http404
from datetime import timedelta
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.utils.dateparse import parse_time
from perfiles.decorators import admin_required
from .forms import PuntualReservationForm, RecurrenteReservationForm
from django.contrib import messages

context = {
    "types_of_service": TypeOfService.objects.all(),
}

def home_view(request):
    return render(request, "home.html", context)


def open_calendar_modal(request, service_name):
    if not request.htmx:
        return HttpResponseBadRequest("Esta vista solo admite peticiones HTMX.")
    try:
        n = TypeOfService.objects.get(name = service_name)
    except TypeOfService.DoesNotExist:
        raise Http404("No hay ningun servicio registrado.")
    return render(request, "modal.html", {"service": n})


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


def disponibilidad_json(request, service_id):
    inicio_str = request.GET.get('mes')
    fin_str = request.GET.get('fin')

    if not inicio_str or not fin_str:
        return JsonResponse([], safe=False)

    inicio = parse_date(inicio_str[:10])
    fin = parse_date(fin_str[:10])

    if not inicio or not fin:
        return JsonResponse([], safe=False)

    try:
        service = TypeOfService.objects.get(id=service_id)
    except TypeOfService.DoesNotExist:
        return JsonResponse([], safe=False)

    slots_del_rango = Reservation.objects.filter(
        service=service,
        date__gte=inicio,
        date__lt=fin
    )

    ahora = timezone.localtime()
    hoy = ahora.date()
    hora_actual = ahora.time()

    resultado = []
    dia = inicio
    while dia < fin:
        if dia < hoy:
            dia += timedelta(days=1)
            continue

        slots_del_dia = [res for res in slots_del_rango if res.date == dia]

        slots_libres = [
            {"id": res.id, "time": res.time_start.strftime("%H:%M"), "end": res.time_end.strftime("%H:%M"),}
            for res in slots_del_dia
            if res.user is None and res.status == Reservation.States.OPEN
        ]
        
        if dia == hoy:
            slots_libres = [
                slot for slot in slots_libres
                if parse_time(slot["time"]) > hora_actual
            ]

        if slots_libres:
            resultado.append({
                "date": dia.isoformat(),
                "horarios": slots_libres,
            })

        dia += timedelta(days=1)

    return JsonResponse(resultado, safe=False)

@admin_required
def admin_interface_view(request):
    return render(request, "admin_interface.html")

@admin_required
def create_reservation_view (request):
    if request.method == 'POST':
        form = PuntualReservationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Reservation.objects.create(
                service=cd['service'],
                date=cd['date'],
                time_start=cd['time_start'],
                time_end=cd['time_end'],
            )
            messages.success(request, "Slot puntual creado.")
            return redirect('interface_admin')
    else:
        form = PuntualReservationForm()
    return render(request, 'create_single_reservation.html', {'form': form})


@admin_required
def create_recurrent_reservations_view(request):
    if request.method == 'POST':
        form = RecurrenteReservationForm(request.POST)
        if form.is_valid():
            regla = form.save()
            regla.generate_reservations()
            messages.success(
                request,
                f"Regla creada y {regla.generated_reservations.count()} slots generados."
            )
            return redirect('interface_admin')
    else:
        form = RecurrenteReservationForm()
    return render(request, 'create_recurrent_reservation.html', {'form': form})