from django.urls import path
from .views import reservation_view
from .views import set_reservation_view

urlpatterns = [
    path('mis_reservas/', reservation_view, name="reservations"),
    path('reservar/<int:reservation_id>/', set_reservation_view, name="reserve"),
]
