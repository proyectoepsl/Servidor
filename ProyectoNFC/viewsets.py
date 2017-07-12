from datetime import datetime
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Registro, Usuario, Sala, Permiso
from .serializer import  UsuarioSerializer, SalaSerializer
from .AESCipher import *

import json
import base64

@csrf_exempt
def UsuarioViewSet(request):
    if request.method == 'GET':
        query = Usuario.objects.all()
        serializer = UsuarioSerializer(query, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        Salaint = data["Sala_id"]
        Salaint = Salaint.rstrip("\n")
        Salaint = AESCipher().decrypt(Salaint)
        Dni = data["Dni"]
        Dni = Dni.rstrip("\n")


        #Desencriptar Mensaje
        Dni = AESCipher().decrypt(Dni)



        # Comprobar si existe el Usuario
        try:
            consulta = Usuario.objects.get(Dni=Dni)

            # Comprobar si el usuario esta activo
            if consulta.Activo:
                try:
                    consulta1 = Permiso.objects.get(Usuario=consulta.Id_Usuario,Sala=int(Salaint))
                except Permiso.DoesNotExist:
                    response_data = {}
                    response_data['result'] = 404
                    response_data['Error'] = "Usuario no tiene permiso para entrar en esta Sala"
                    return HttpResponse(json.dumps(response_data), content_type="application/json",status=404)

                # Consultar si el usuario tiene permiso
                if consulta1.Permiso:
                        # Consultar el aforo
                        consulta2 = Sala.objects.get(Id_Sala=int(Salaint))
                        # Consultar el aforo
                        if consulta2.Aforo > 0:
                            #Descontar uno al aforo
                            consulta2.Aforo -= 1
                            consulta2.save()
                            #Comprobar si registro es de entrada o de salida

                            try:
                                consulta3 = Registro.objects.get(Usuario_id=int(consulta.Id_Usuario), Sala_id=int(Salaint),Terminado=False)
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
                                    consulta2.Aforo += 2
                                    consulta2.save()
                                    response_data = {}
                                    response_data['result'] = 200
                                    response_data['IdSala'] = consulta2.Id_Sala
                                    response_data['IdUsuario'] = consulta.Id_Usuario
                                    return HttpResponse(json.dumps(response_data), content_type="application/json",
                                                        status=200)

                            except Registro.DoesNotExist:
                                # Es registro de entrada
                                datos = Registro(
                                    Sala_id=int(Salaint),
                                    Usuario_id=int(consulta.Id_Usuario)
                                )
                                datos.save()
                                response_data = {}
                                response_data['result'] = 200
                                response_data['IdSala'] = consulta2.Id_Sala
                                response_data['IdUsuario'] = consulta.Id_Usuario
                                return HttpResponse(json.dumps(response_data), content_type="application/json")

                        else:
                            response_data = {}
                            response_data['result'] = 403
                            response_data['Error'] = "Sala ocupada"
                            return HttpResponse(json.dumps(response_data), content_type="application/json",status=403)


                else:
                    response_data = {}
                    response_data['result'] = 403
                    response_data['Error'] = "El usuario no tiene permisos"
                    return HttpResponse(json.dumps(response_data), content_type="application/json",status=403)


            else:
                response_data = {}
                response_data['result'] = 401
                response_data['Error'] = "El usuario esta desactivado"
                return HttpResponse(json.dumps(response_data), content_type="application/json",status=401)


        except Usuario.DoesNotExist:
            response_data = {}
            response_data['result'] = 401
            response_data['Error'] = "Usuario no existe"
            return HttpResponse(json.dumps(response_data), content_type="application/json",status=401)



@csrf_exempt
def SalaViewSet(request):
    if request.method == 'GET':
        query = Sala.objects.all()
        serializer = SalaSerializer(query, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        #data = JSONParser().parse(request)
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)

        try:
            # Guardo el dato que me llega del Json
            Hash = data["Hash"]
            # Quito el \n al mensaje
            Hash = Hash.rstrip("\n")

            #Añado b' al Hash
            Hash1 ="b'{0}'"
            Hash2=Hash1.format(Hash)

             # Desencriptar Mensaje
            mensajeDesencriptado = AESCipher().decrypt(Hash)

        except :
            response_data = {}
            response_data['result'] = 500
            response_data['Error'] = "Mensaje no ha podido ser descifrado"
            return HttpResponse(json.dumps(response_data), content_type="application/json",status=500)

        # Comprobar si existe el imei
        try:
            consulta = Sala.objects.get(Hash=mensajeDesencriptado)
            # Comprobar que esta activa la sala


            if consulta.Activo:
                #Si esta activa la sala le devuelvo mensaje de confirmacion y le mando los datos para identificar la sala
                response_data = {}
                response_data['result'] = 200
                response_data['IdSala'] = consulta.Id_Sala
                response_data['Dependencia'] = consulta.Dependencia
                #Open crea la imagen en array de bit(rb)
                #Codificar en ASCII
                #Base64 formatea el ASCII que ya es reconocido por JSON
                response_data['Plano'] = base64.encodestring(open(consulta.Plano.path, 'rb').read()).decode('ascii')
                return HttpResponse(json.dumps(response_data), content_type="application/json",status=200)
            #Si la sala no esta activa,le envio un error al usuario
            else:
                response_data = {}
                response_data['result'] = 404
                response_data['Error'] = "La sala no esta activa "
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=404)
        #El imei que tiene ese dispositivo no esta almacenado en la base de datos.
        except Sala.DoesNotExist:
            response_data = {}
            response_data['result'] = 404
            response_data['Error'] = "Imei no existe en la base de datos"
            return HttpResponse(json.dumps(response_data), content_type="application/json",status=404)