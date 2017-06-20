from __future__ import unicode_literals
from django.contrib import admin
from .models import Sala,Usuario,Registro

class AdminSala (admin.ModelAdmin):
    list_display = ['Id_Sala','Nombre','Hash','Aforo','Activo']
    list_editable = ['Nombre','Hash','Activo']
    search_fields = ['Id_Sala','Nombre','Hash','Aforo','Activo']

admin.site.register(Sala,AdminSala)

class AdminUsuario (admin.ModelAdmin):
    list_display = ['Id_Usuario','Nombre','Apellidos','Dni','Clave','Activo']
    list_editable = ['Nombre','Apellidos','Clave','Activo']
    search_fields = ['Id_Usuario','Nombre','Apellidos','Dni','Activo']

admin.site.register(Usuario,AdminUsuario)


class AdminRegistro (admin.ModelAdmin):
    list_display = ['Id_Registro','Sala','Usuario','Fecha_In','Fecha_Out']
    search_fields = ['Id_Registro','Sala','Usuario','Fecha_In','Fecha_Out']


admin.site.register(Registro, AdminRegistro)
