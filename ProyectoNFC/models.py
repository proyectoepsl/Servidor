from __future__ import unicode_literals
from django.db import models


class Sala (models.Model):
    Id_Sala = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=50, unique=True)
    Hash =models.CharField(max_length=30)
    Aforo = models.IntegerField(null= True)
    Activo = models.BooleanField(default= False)

    def __str__(self):
        return (self.Nombre)

class Usuario (models.Model):
    Id_Usuario = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=30)
    Apellidos = models.CharField(max_length=30)
    Dni=models.CharField(max_length=9)
    Clave = models.CharField(max_length=30,unique=True)
    Activo = models.BooleanField(default=False)

    def __str__(self):
        return (self.Nombre)

class Registro (models.Model):
    Id_Registro = models.AutoField(primary_key=True)
    Sala =  models.ForeignKey('Sala')
    Usuario = models.ForeignKey('Usuario')
    Fecha_In = models.DateTimeField(auto_now_add=True,auto_now=False,null=True)
    Fecha_Out = models.DateTimeField(auto_now_add=False,auto_now=True,null=True)


