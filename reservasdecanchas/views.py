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

#vista que retorna el calendario de reservas de un servicio para ingresarlo al modal
def open_calendar_modal(request, service_name):
    if not request.htmx:
        return HttpResponseBadRequest("Esta vista solo admite peticiones HTMX.")
    try:
        n = TypeOfService.objects.get(name = service_name)
    except TypeOfService.DoesNotExist:
        raise Http404("No hay ningun servicio registrado.")
    return render(request, "modal.html", {"service": n})


#vista que devuelve un json con los eventos del calendario
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

#vista que devuelve un json con los slots del mes libres
def disponibilidad_json(request, service_id):
    #se obtiene del mes en el que se encuentra el calendario
    inicio_str = request.GET.get('mes')
    #y el fin del mes
    fin_str = request.GET.get('fin')

    if not inicio_str or not fin_str:
        return JsonResponse([], safe=False)
    #se parsea la fecha de inicio y de fin
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
    hora_actual = timezone.localtime().time()
    if hora_actual.tzinfo is not None:
        hora_actual = hora_actual.replace(tzinfo=None)

    resultado = []
    dia = inicio

    #bucle que recorre el mes dia por dia
    while dia < fin:
        #se salta los dias pasados
        if dia < hoy:
            dia += timedelta(days=1)
            continue

        #se obtiene los slots del dia
        slots_del_dia = [res for res in slots_del_rango if res.date == dia]

        #se obtiene los slots libres
        slots_libres = [
            {"id": res.id, "time": res.time_start.strftime("%H:%M"), "end": res.time_end.strftime("%H:%M"),}
            for res in slots_del_dia
            if res.user is None and res.status == Reservation.States.OPEN
        ]
        
        #si el dia es hoy, se filtra los slots que ya pasaron
        if dia == hoy:
            slots_libres = [
                slot for slot in slots_libres
                if parse_time(slot["time"]) > hora_actual
            ]

        #si hay slots libres
        if slots_libres:
            #se agrega al resultado
            resultado.append({
                "date": dia.isoformat(),
                "horarios": slots_libres,
            })

        dia += timedelta(days=1)

    return JsonResponse(resultado, safe=False)

@admin_required
def admin_interface_view(request):
    return render(request, "admin_interface.html")

#vista que crea un slot puntual o renderiza el formulario para crearlo
@admin_required
def create_reservation_view (request):
    if request.method == 'POST':
        #se guarda el formulario si es valido
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
        #si no es POST, se renderiza el formulario
        form = PuntualReservationForm()
    return render(request, 'create_single_reservation.html', {'form': form})

#vista que crea slots recurrentes o renderiza el formulario para crearlos
@admin_required
def create_recurrent_reservations_view(request):
    if request.method == 'POST':
        #se guarda el formulario si es valido
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