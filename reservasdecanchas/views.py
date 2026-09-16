from django.shortcuts import render
from tipo_de_servicio.models import TypeOfService

context = {
    "types_of_service": TypeOfService.objects.all(),

}

def home_view(request):
    return render(request, "home.html", context)