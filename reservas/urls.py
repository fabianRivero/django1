from django.urls import path
from .views import reservation_view

urlpatterns = [
    path('mis_reservas/', reservation_view, name="reservations"),
]
