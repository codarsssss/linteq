from django.contrib import admin
from .models import Consultation


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message', 'date']
    list_filter = ['date', 'name']
    search_fields = ['name', 'email', 'subject', 'message', 'date']
    ordering = ['name', 'date']
    readonly_fields = ['name', 'email', 'subject', 'message', 'date']
