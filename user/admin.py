from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone  # Importa timezone para trabajar con fechas y horas
from .models import CustomUser

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'dni', 'celular','genero', 'fecha_de_registro', 'is_staff', 'is_active', 'foto_de_perfil',)
    search_fields = ('username', 'email', 'dni', 'celular', 'genero',)
    list_filter = ('is_staff', 'is_active', 'fecha_registro', 'genero',)

    @admin.display() 
    def fecha_de_registro(self, obj):  
        if obj.fecha_registro:
            return obj.fecha_registro.strftime("%d-%m-%Y %H:%M:%S")  # Formatea la fecha como día-mes-año hora:minuto:segundo
        return '-'  # Devuelve un guion si no hay fecha de registro

    @admin.display()
    def foto_de_perfil(self, obj):
        if obj.foto_perfil:
            return format_html(
                '<div style="display: flex; justify-content: center;"><img src="{}" width="50" height="50" style="border-radius: 50%;"/></div>',
                obj.foto_perfil.url
            )
        return '-'

admin.site.register(CustomUser, CustomUserAdmin)
