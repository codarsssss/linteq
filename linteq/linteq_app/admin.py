from django.contrib import admin
from .models import Consultation, FileData
from django.contrib.auth.models import User, Group


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message', 'date']
    list_filter = ['date', 'name']
    search_fields = ['name', 'email', 'subject', 'message', 'date']
    ordering = ['name', 'date']
    readonly_fields = ['name', 'email', 'subject', 'message', 'date']


@admin.register(FileData)
class FileDataAdmin(admin.ModelAdmin):
    list_display = ['create_date', 'delete_date']
    list_filter = ['create_date', 'delete_date']
    search_fields = ['create_date', 'delete_date']
    ordering = ['create_date', 'delete_date']
    readonly_fields = ['path', 'create_date', 'delete_date']


admin.site.unregister(User)

admin.site.unregister(Group)
