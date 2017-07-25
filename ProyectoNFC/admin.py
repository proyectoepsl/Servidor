from __future__ import unicode_literals
from django.contrib import admin
from .models import Sala,Usuario,Registro,Permiso

class AdminSala (admin.ModelAdmin):
    list_display = ['Id_Sala','Nombre','Hash','Aforo','Aforo_Maximo','Activo','Plano1','Dependencia']
    list_editable = ['Nombre','Hash','Activo','Aforo','Aforo_Maximo','Dependencia']
    search_fields = ['Id_Sala','Nombre','Hash','Aforo','Activo','Aforo_Maximo','Dependencia']

admin.site.register(Sala,AdminSala)

class AdminUsuario (admin.ModelAdmin):
    list_display = ['Id_Usuario','Nombre','Apellidos','Dni','Activo']
    list_editable = ['Nombre','Apellidos','Activo']
    search_fields = ['Id_Usuario','Nombre','Apellidos','Dni','Activo']

admin.site.register(Usuario,AdminUsuario)


class AdminRegistro (admin.ModelAdmin):
    list_display = ['Id_Registro','Sala','Usuario','Fecha_In','Fecha_Out','Terminado']
    search_fields = ['Id_Registro','Sala','Usuario','Fecha_In','Fecha_Out','Terminado']
    list_filter = ['Fecha_In','Fecha_Out']

admin.site.register(Registro, AdminRegistro)

class AdminPermisos (admin.ModelAdmin):
    list_display = ['Id_Permiso','Sala','Usuario','Permiso']
    list_editable = ['Sala','Usuario','Permiso']
    search_fields = ['Id_Permiso', 'Sala', 'Usuario', 'Permiso']

admin.site.register(Permiso, AdminPermisos)
