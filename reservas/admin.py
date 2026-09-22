from django.contrib import admin
from .models import Reservation, RecurringReservation
from .forms import RecurringReservationForm


@admin.register(RecurringReservation)
class RecurringReservationAdmin(admin.ModelAdmin):
    form = RecurringReservationForm
    list_display = ("id", "rule_type", "start_date", "end_date", "service")
    list_filter = ("rule_type", "service")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "time_start", "time_end", "service", "status", "user")
    list_filter = ("status", "service", "date")
    search_fields = ("user__username", "service__name")