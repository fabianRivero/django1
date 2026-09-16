from django.contrib import admin
from .models import TypeOfService

@admin.register(TypeOfService)
class TypeOfServiceAdmin(admin.ModelAdmin):
    list_display = ['name']

