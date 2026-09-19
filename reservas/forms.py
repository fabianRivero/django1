from django import forms
from datetime import datetime
from .models import RecurringReservation
from tipo_de_servicio.models import TypeOfService
from django.utils import timezone

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

    class Media:
        js = ('admin/js/recurring_reservation.js',)

    def clean_days_of_week(self):
        data = self.cleaned_data.get("days_of_week", [])
        return list(map(int, data))



class TakeRecurringReservationForm(forms.Form):
    
    service = forms.ModelChoiceField(
        queryset=TypeOfService.objects.all(),
        widget=forms.RadioSelect,
        label="Servicio",
        empty_label=None 
    )

    year = forms.ChoiceField(
        choices=[
            (datetime.now().year, str(datetime.now().year)),
            (datetime.now().year + 1, str(datetime.now().year + 1)),
        ],
        label="Año"
    )

    month = forms.ChoiceField(
        choices=RecurringReservation.MONTHS,
        label="Mes"
    )

    weeks = forms.IntegerField(
        min_value=1,
        max_value=6,
        initial=4,
        label="Cantidad de semanas"
    )

    weekday = forms.ChoiceField(
        choices=RecurringReservation.DAYS_OF_WEEK,
        label="Día de la semana"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_year = timezone.now().year
        self.fields['year'].choices = [
            (current_year, str(current_year)),
            (current_year + 1, str(current_year + 1)),
        ]

class TakeRecurringReservationConfirmForm(forms.Form):
    selected_group = forms.CharField(widget=forms.HiddenInput)
    time_range = forms.CharField(widget=forms.HiddenInput, required=False)