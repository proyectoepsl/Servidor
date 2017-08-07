from datetime import datetime
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Registro, Usuario, Sala, Permiso
from .serializer import UsuarioSerializer, SalaSerializer
from .AESCipher import *

import json
import base64


@csrf_exempt
def UsuarioViewSet(request):
    if request.method == 'GET':
        query = Usuario.objects.all()
        serializer = UsuarioSerializer(query, many=True)
        return JsonResponse(serializer.data, safe=False)
    #Peticion POST
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        Salaint = data["Sala_id"]
        Salaint = Salaint.rstrip("\n")
        Sala=int = AESCipher().decrypt(Salaint)
        Dni = data["Dni"]
        Dni = Dni.rstrip("\n")
        Dni = AESCipher().decrypt(Dni)

        # Comprobar si existe el Usuario
        try:
            consulta = Usuario.objects.get(Dni=Dni)

            # Comprobar si el usuario esta activo
            if consulta.Activo:
                try:
                    consulta1 = Permiso.objects.get(Usuario=consulta.Id_Usuario, Sala=int(Salaint))
                except Permiso.DoesNotExist:
                    response_data = {}
                    response_data['result'] = 404
                    response_data['Error'] = "Usuario no tiene permiso para entrar en esta Sala"
                    return HttpResponse(json.dumps(response_data), content_type="application/json", status=404)

                # Consultar si el usuario tiene permiso
                if consulta1.Permiso:
                    # Consultar el todos los datos de mi sala
                    consulta2 = Sala.objects.get(Id_Sala=int(Salaint))
                # Comprobar si registro es de entrada o de salida

                    try:
                        consulta3 = Registro.objects.get(Usuario_id=int(consulta.Id_Usuario), Sala_id=int(Salaint),
                                                         Terminado=False)
                        # El registro es de salida
                        if consulta3.Fecha_Out == None:
                            datos = Registro(
                                Id_Registro=consulta3.Id_Registro,
                                Sala_id=consulta3.Sala_id,
                                Usuario_id=consulta3.Usuario_id,
                                Fecha_In=consulta3.Fecha_In,
                                Fecha_Out=datetime.now(),
                                Terminado=True
                            )
                            datos.save()
                            consulta2.Aforo -= 1
                            consulta2.save()
                            response_data = {}
                            response_data['result'] = 200
                            response_data['IdSala'] = consulta2.Id_Sala
                            response_data['IdUsuario'] = consulta.Id_Usuario
                            response_data['Error'] = 'Hasta Pronto'

                            return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)

                    except Registro.DoesNotExist:
                        # Consultar aforo
                        if consulta2.Aforo < consulta2.Aforo_Maximo:
                            # Es registro de entrada
                            datos = Registro(
                                Sala_id=int(Salaint),
                                Usuario_id=int(consulta.Id_Usuario)
                            )
                            datos.save()
                            consulta2.Aforo += 1
                            consulta2.save()
                            response_data = {}
                            response_data['result'] = 200
                            response_data['IdSala'] = consulta2.Id_Sala
                            response_data['IdUsuario'] = consulta.Id_Usuario
                            response_data['Error'] = 'Bienvenido'
                            return HttpResponse(json.dumps(response_data), content_type="application/json")
                        #Aforo completo
                        else:
                            response_data = {}
                            response_data['result'] = 403
                            response_data['Error'] = "Sala completa"
                            return HttpResponse(json.dumps(response_data), content_type="application/json", status=403)



                else:
                    response_data = {}
                    response_data['result'] = 403
                    response_data['Error'] = "El usuario no tiene permisos"
                    return HttpResponse(json.dumps(response_data), content_type="application/json", status=403)


            else:
                response_data = {}
                response_data['result'] = 401
                response_data['Error'] = "El usuario esta desactivado"
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)

        except Usuario.DoesNotExist:
            response_data = {}
            response_data['result'] = 401
            response_data['Error'] = "Usuario no existe"
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)


@csrf_exempt
def SalaViewSet(request):
    if request.method == 'GET':
        query = Sala.objects.all()
        serializer = SalaSerializer(query, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        # data = JSONParser().parse(request)
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)

        try:
            # Guardo el dato que me llega del Json
            Hash = data["Hash"]
            # Quito el \n al mensaje
            Hash = Hash.rstrip("\n")

            # Añado b' al Hash
            Hash1 = "b'{0}'"
            Hash2 = Hash1.format(Hash)

            # Desencriptar Mensaje
            mensajeDesencriptado = AESCipher().decrypt(Hash)

        except:
            response_data = {}
            response_data['result'] = 500
            response_data['Error'] = "Mensaje no ha podido ser descifrado"
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=500)

        # Comprobar si existe el imei
        try:
            consulta = Sala.objects.get(Hash=mensajeDesencriptado)
            # Comprobar que esta activa la sala


            if consulta.Activo:
                # Si esta activa la sala le devuelvo mensaje de confirmacion y le mando los datos para identificar la sala
                response_data = {}
                response_data['result'] = 200
                response_data['IdSala'] = consulta.Id_Sala
                response_data['Capacidad'] = consulta.Aforo_Maximo
                response_data['Aforo'] = consulta.Aforo
                response_data['Dependencia'] = consulta.Dependencia
                # Open crea la imagen en array de bit(rb)
                # Codificar en ASCII
                # Base64 formatea el ASCII que ya es reconocido por JSON
                response_data['Plano'] = base64.encodestring(open(consulta.Plano.path, 'rb').read()).decode('ascii')
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)
            # Si la sala no esta activa,le envio un error al usuario
            else:
                response_data = {}
                response_data['result'] = 404
                response_data['Error'] = "La sala no esta activa "
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=404)
        # El imei que tiene ese dispositivo no esta almacenado en la base de datos.
        except Sala.DoesNotExist:
            response_data = {}
            response_data['result'] = 404
            response_data['Error'] = "Imei no existe en la base de datos"
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=404)


@csrf_exempt
def LoginViewSet(request):
    if request.method == 'POST':
        # data = JSONParser().parse(request)
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        # Guardo el dato que me llega del Json
        try:
            # Guardo el dato que me llega del Json
            Username = data["username"]
            Password = data["password"]
            try:
                # Quito el \n al mensaje
                Username = Username.rstrip("\n")
                Password = Password.rstrip("\n")
                # Desencriptar Mensaje
                username = AESCipher().decrypt(Username)
                password = AESCipher().decrypt(Password)


            # Confirmo si el usuario esta autentificado
                user = authenticate(username=username,password=password)
                #password = check_password(password)
                if user is not None and user.is_active:
                   response_data = {}
                   response_data['result'] = 200
                   response_data['Error'] = "Datos de usuario correcto"
                   return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)
                else:
                   response_data = {}
                   response_data['result'] = 404
                   response_data['Error'] = "Datos de usuario incorrectos"
                   return HttpResponse(json.dumps(response_data), content_type="application/json", status=404)

            except:
                response_data = {}
                response_data['result'] = 500
                response_data['Error'] = "Mensaje no ha podido ser descifrado"
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=500)
        except:
            response_data = {}
            response_data['result'] = 500
            response_data['Error'] = "No se han recibido datos de login"
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=500)

@csrf_exempt
def ModPassViewSet(request):
 if request.method == 'POST':
        # data = JSONParser().parse(request)
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        # Guardo el dato que me llega del Json
        try:
            # Guardo el dato que me llega del Json
            Username = data["username"]
            Password = data["password"]
            try:
                # Quito el \n al mensaje
                Username = Username.rstrip("\n")
                Password = Password.rstrip("\n")
                # Desencriptar Mensaje
                mensajeDesencriptado1 = AESCipher().decrypt(Username)
                mensajeDesencriptado2 = AESCipher().decrypt(Password)

                # Confirmo si el usuario esta autentificado
                try:
                    user = User.objects.get(username=mensajeDesencriptado1)
                    user.set_password(mensajeDesencriptado2)
                    user.save()
                    response_data = {}
                    response_data['result'] = 200
                    response_data['Error'] = "Password modificado"
                    return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)
                except User.DoesNotExist:
                    response_data = {}
                    response_data['result'] = 404
                    response_data['Error'] = "Usuario no existe en la Base de Datos"
                    return HttpResponse(json.dumps(response_data), content_type="application/json", status=404)

            except:
                response_data = {}
                response_data['result'] = 500
                response_data['Error'] = "Mensaje no ha podido ser descifrado"
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=500)
        except:
            response_data = {}
            response_data['result'] = 500
            response_data['Error'] = "No se han recibido datos de Usuario"
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=500)
@csrf_exempt
def ModUserViewSet(request):
    if request.method == 'POST':
        # data = JSONParser().parse(request)
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        # Guardo el dato que me llega del Json
        try:
            # Guardo el dato que me llega del Json
            Username = data["usernamepref"]
            UsernameMOD = data["username"]
            try:
                # Quito el \n al mensaje
                Username = Username.rstrip("\n")
                UsernameMOD = UsernameMOD.rstrip("\n")
                # Desencriptar Mensaje
                mensajeDesencriptado1 = AESCipher().decrypt(Username)
                mensajeDesencriptado2 = AESCipher().decrypt(UsernameMOD)


            # Confirmo si el usuario esta autentificado
                try:
                    user = User.objects.get(username=mensajeDesencriptado1)
                    user.username=mensajeDesencriptado2
                    user.save()
                    response_data = {}
                    response_data['result'] = 200
                    response_data['Error'] = "Usuario modificado"
                    return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)
                except User.DoesNotExist:
                    response_data = {}
                    response_data['result'] = 404
                    response_data['Error'] = "Usuario no existe en la Base de Datos"
                    return HttpResponse(json.dumps(response_data), content_type="application/json", status=404)

            except:
                response_data = {}
                response_data['result'] = 500
                response_data['Error'] = "Mensaje no ha podido ser descifrado"
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=500)
        except:
            response_data = {}
            response_data['result'] = 500
            response_data['Error'] = "No se han recibido datos de Usuario"
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=500)

