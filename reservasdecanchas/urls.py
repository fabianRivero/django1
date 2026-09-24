from django.contrib import admin
from django.urls import path, include
from .views import home_view, open_calendar_modal, eventos_json, disponibilidad_json, admin_interface_view, create_recurrent_reservations_view, create_reservation_view
from perfiles import urls as perfiles_urls
from reservas import urls as reservas_urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home_view, name="home"),
    path('calendario/modal/<str:service_name>/', open_calendar_modal, name='open_calendar_modal'),
    path('api/eventos/', eventos_json, name='eventos_json'),
    path('api/disponibilidad/<int:service_id>/', disponibilidad_json, name='disponibilidad_json'),
    path("", include(reservas_urls)),
    path("", include(perfiles_urls)),
    path("interfaz_admin/", admin_interface_view, name="interface_admin"),
    path('interfaz_admin/puntual/', create_reservation_view, name='crear_puntual'),
    path('interfaz_admin/recurrente/', create_recurrent_reservations_view, name='crear_recurrente'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)