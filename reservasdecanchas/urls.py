from django.contrib import admin
from django.urls import path, include
from .views import home_view, open_calendar_modal, eventos_json
from perfiles import urls as perfiles_urls
from reservas import urls as reservas_urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home_view, name="home"),
    path('calendario/modal/<str:service_name>/', open_calendar_modal, name='open_calendar_modal'),
    path('api/eventos/', eventos_json, name='eventos_json'),
    path("", include(reservas_urls)),
    path("", include(perfiles_urls)),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)