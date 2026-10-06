from datetime import timedelta
from django import forms
from django.utils import timezone
from tipo_de_servicio.models import TypeOfService
from reservas.models import RecurringReservation

#formulario para crear reserva puntual
class PuntualReservationForm(forms.Form):
    service = forms.ModelChoiceField(
        queryset=TypeOfService.objects.all(),
        label="Servicio",
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha",
    )
    time_start = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label="Hora de inicio",
    )
    time_end = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label="Hora de finalización",
    )

    #metodo que valida el formulario
    def clean(self):
        cleaned = super().clean()
        date = cleaned.get('date')
        time_start = cleaned.get('time_start')
        time_end = cleaned.get('time_end')

        if date and date < timezone.localtime().date():
            raise forms.ValidationError("No puedes crear reservas en el pasado.")

        if time_start and time_end and time_end <= time_start:
            raise forms.ValidationError("La hora de fin debe ser posterior a la de inicio.")

        return cleaned


class RecurrenteReservationForm(forms.ModelForm):
    days_of_week = forms.MultipleChoiceField(
        choices=RecurringReservation.DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Días de la semana (solo si es semanal)",
    )

    class Meta:
        model = RecurringReservation
        fields = [
            'service',
            'rule_type',
            'days_of_week',
            'start_date',
            'end_date',
            'time_start',
            'time_end',
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'time_start': forms.TimeInput(attrs={'type': 'time'}),
            'time_end': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned = super().clean()
        rule_type = cleaned.get('rule_type')
        days = cleaned.get('days_of_week') or []
        start = cleaned.get('start_date')
        end = cleaned.get('end_date')

        if rule_type == 'weekly' and not days:
            raise forms.ValidationError(
                "Para una regla semanal tienes que elegir uno o varios dias."
            )

        if start and end:
            if end < start:
                raise forms.ValidationError("La fecha de fin debe ser posterior a la de inicio.")
            if (end - start) > timedelta(days=180):
                raise forms.ValidationError("El rango máximo es de 180 días.")
            if start < timezone.localtime().date():
                raise forms.ValidationError("La fecha de inicio no puede ser en el pasado.")

        return cleaned

    def clean_days_of_week(self):
        data = self.cleaned_data.get('days_of_week') or []
        return list(map(int, data))