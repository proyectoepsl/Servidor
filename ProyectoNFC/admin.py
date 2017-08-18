from __future__ import unicode_literals
from django.contrib import admin

from suit.admin import SortableModelAdmin
from .models import Sala,Usuario,Registro,Permiso

class AdminSala (admin.ModelAdmin):
    list_display = ['Id_Sala','Nombre','Aforo','Activo','Aforo_Maximo','Dependencia','Plano1']
    list_editable = ['Activo','Aforo']
    search_fields = ['Id_Sala','Nombre','Imei','Dependencia']
    list_filter = ['Aforo','Activo']
admin.site.register(Sala,AdminSala)

class AdminUsuario (admin.ModelAdmin):
    list_display = ['Id_Usuario','Nombre','Apellidos','Dni','Activo']
    list_editable = ['Activo']
    search_fields = ['Nombre','Apellidos','Dni']
    list_filter = ['Activo']

admin.site.register(Usuario,AdminUsuario)


class AdminRegistro (admin.ModelAdmin):
    list_display = ['Id_Registro','Sala','Usuario','Fecha_In','Fecha_Out','Terminado']
    list_editable = ['Terminado']
    list_filter = ['Sala','Usuario','Fecha_In','Fecha_Out','Terminado']

admin.site.register(Registro, AdminRegistro)

class AdminPermisos (admin.ModelAdmin):
    list_display = ['Id_Permiso','Sala','Usuario','Permiso']
    list_editable = ['Permiso']
    list_filter = ['Sala','Usuario','Permiso']
admin.site.register(Permiso, AdminPermisos)
