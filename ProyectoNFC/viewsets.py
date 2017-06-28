from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .models import Registro, Usuario, Sala, Permiso
from .serializer import RegistroSerializer, UsuarioSerializer, SalaSerializer
from .AESCipher import *

import json


@csrf_exempt
def RegistroViewSet(request):
    if request.method == 'GET':

        query = Registro.objects.all()
        serializer = RegistroSerializer(query, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        print('-----------------------')
        print(data)
        print(data["Sala_id"])
        print(data["Usuario_id"])
        print('-----------------------')
        '''
        serializer = RegistroSerializer(data=request)
        print('-----------------------')
        print(repr(serializer))
        print('-----------------------')
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)

        '''

        '''
        try:
            Usuario.objects.get(Id_Usuario=data["Usuario_id"])
            Sala.objects.get(Id_Sala=data["Sala_id"])
            datos=Registro(
                Sala_id=data["Sala_id"],
                Usuario_id= data["Usuario_id"]
            )
            serializer = RegistroSerializer(data=request)
            if serializer.is_valid():
                serializer.save()
            return JsonResponse(data,status=201)


        except:
            return JsonResponse(data, status=400)

        '''


@csrf_exempt
def UsuarioViewSet(request):
    if request.method == 'GET':
        query = Usuario.objects.all()
        serializer = UsuarioSerializer(query, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        Salaint = data["Sala_id"]
        # Guardo el dato que me llega del Json
        Dni = data["Dni"]
        # Quito el \n al mensaje
        Dni = Dni.rstrip("\n")

        # Desencriptar Mensaje
        # mensajeDesencriptado = AESCipher().decrypt(Dni)
        # Comprobar si existe el Usuario
        try:
            consulta = Usuario.objects.get(Dni=Dni)

            # Comprobar si el usuario esta activo
            if consulta.Activo:
                try:
                    consulta1 = Permiso.objects.get(Usuario=consulta.Id_Usuario)
                except Permiso.DoesNotExist:
                    return HttpResponse("Usuario no existe en la tabla permisos", status=404)
                    # Consultar si el usuario tiene permisos para esa sala

                if consulta1.Permiso:
                    print(consulta1.Sala_id)

                    if consulta1.Sala_id== int(Salaint):
                        print("Hoal")
                        consulta2 = Sala.objects.get(Id_Sala=int(Salaint))
                        # Consultar el aforo
                        if consulta2.Aforo > 0:
                            consulta2.Aforo = consulta2.Aforo - 1
                            response_data = {}
                            response_data['result'] = 200
                            response_data['IdSala'] = consulta2.Id_Sala
                            response_data['IdUsuario'] = consulta.Id_Usuario
                            return HttpResponse(json.dumps(response_data), content_type="application/json")

                        else:

                            return HttpResponse("Sala ocupada", status=404)
                    else:
                        return HttpResponse("En esta sala no puede entrar este Usuario", status=404)
                else:
                    return HttpResponse("El usuario no tiene permisos", status=401)

            else:
                return HttpResponse("El usuario esta desactivado", status=404)
        except Usuario.DoesNotExist:
            return HttpResponse("Usuario no existe", status=404)


@csrf_exempt
def SalaViewSet(request):
    if request.method == 'GET':
        query = Sala.objects.all()
        serializer = SalaSerializer(query, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)

        # Guardo el dato que me llega del Json
        Hash = data["Hash"]
        # Quito el \n al mensaje
        Hash = Hash.rstrip("\n")
        '''
        #Añado b' al Hash
        Hash1 ="b'{0}'"
        Hash2=Hash1.format(Hash)
        '''
        # Desencriptar Mensaje
        mensajeDesencriptado = AESCipher().decrypt(Hash)
        # Comprobar si existe el imei
        try:
            consulta = Sala.objects.get(Hash=mensajeDesencriptado)
            # Comprobar que esta activa la sala y sino la activo

            response_data = {}
            response_data['result'] = 200
            response_data['IdSala'] = consulta.Id_Sala
            if consulta.Activo:
                return HttpResponse(json.dumps(response_data), content_type="application/json")

            else:
                consulta.Activo = True
                consulta.save()
                return HttpResponse(json.dumps(response_data), content_type="application/json")

        except Sala.DoesNotExist:
            return HttpResponse("Imei no existe en la base de datos", status=404)
