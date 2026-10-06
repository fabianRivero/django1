from django import forms
from datetime import datetime
from .models import RecurringReservation
from tipo_de_servicio.models import TypeOfService
from django.utils import timezone

# formulario para crear reservas recurrentes
class RecurringReservationForm(forms.ModelForm):
    days_of_week = forms.MultipleChoiceField(
        choices=RecurringReservation.DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Días de la semana"
    )

    class Meta:
        model = RecurringReservation
        fields = "__all__"

    #class media para asociar el js estatico que necesita el formulario
    class Media:
        js = ('admin/js/recurring_reservation.js',)

    
    def clean_days_of_week(self):
        #se obtiene los dias marcados con el checkbox
        data = self.cleaned_data.get("days_of_week", [])
        return list(map(int, data))
