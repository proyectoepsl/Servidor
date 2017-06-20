
from .models import Registro,Usuario,Sala
from rest_framework import  serializers

# Serializers define the API representation.
class RegistroSerializer (serializers.ModelSerializer):
    class Meta:
        model = Registro
        fields = ('Id_Registro','Sala_id','Usuario_id','Fecha_In','Fecha_Out')

class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Usuario
        fields = ('Id_Usuario','Nombre','Apellidos','Dni','Clave','Activo')

class SalaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sala
        fields = ('Id_Sala','Nombre','Hash','Aforo','Activo')

