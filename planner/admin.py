"""
Configuracion del panel de administracion para los modelos de planner.
"""
from django.contrib import admin
from .models import MediaPost, AgendaItem


@admin.register(MediaPost)
class MediaPostAdmin(admin.ModelAdmin):
    """
    Admin para gestionar las imagenes subidas por los usuarios.
    """
    list_display = ['user', 'order', 'uploaded_at']
    list_filter = ['user']


@admin.register(AgendaItem)
class AgendaItemAdmin(admin.ModelAdmin):
    """
    Admin para gestionar los items de la agenda semanal.
    """
    list_display = ['user', 'title', 'post_type', 'day', 'time']
    list_filter = ['user', 'day', 'post_type']
