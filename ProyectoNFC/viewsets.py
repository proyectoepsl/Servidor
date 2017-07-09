from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .models import Registro, Usuario, Sala, Permiso
from .serializer import RegistroSerializer, UsuarioSerializer, SalaSerializer
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
                    consulta1 = Permiso.objects.get(Usuario=consulta.Id_Usuario)
                except Permiso.DoesNotExist:
                    return HttpResponse("Usuario no existe en la tabla permisos", status=404)
                # Consultar si el usuario tiene permiso
                if consulta1.Permiso:
                    #Consultar si es la sala donde quiere entrar si es donde tiene los permisos
                    if consulta1.Sala_id== int(Salaint):
                        consulta2 = Sala.objects.get(Id_Sala=int(Salaint))
                        # Consultar el aforo
                        if consulta2.Aforo > 0:
                            #Descontar uno al aforo
                            consulta2.Aforo -= 1
                            consulta2.save()
                            #Comprobar si registro es de entrada o de salida
                            '''
                            try:
                                consulta3 = Registro.objects.all(Usuario_id=consulta.Id_Usuario)
                                if consulta3.Sala_id==int(Salaint):
                                    print(consulta3.Fecha_In)
                                    print(consulta3.Fecha_Out)
                                    if consulta3.Fecha_In==consulta3.Fecha_Out:
                                        #Si la fecha de entrada es igual que la de salida el registro que hay guardado es el de entrada
                                        consulta3.update()

                                        response_data = {}
                                        response_data['result'] = 200
                                        response_data['IdSala'] = consulta2.Id_Sala
                                        response_data['IdUsuario'] = consulta.Id_Usuario
                                        return HttpResponse(json.dumps(response_data), content_type="application/json")
                                    else:
                                        #Se crea un nuevo registro por que es una nueva entrada del usuario
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
                                    #Es el primer paso de este usuario en esta sala
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


                            except Registro.DoesNotExist:
                                #Es el primer paso del usuario
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
                            '''
                            #Guardar datos en Registro Nuevo
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
                            return HttpResponse(json.dumps(response_data), content_type="application/json")

                    else:
                        response_data = {}
                        response_data['result'] = 403
                        response_data['Error'] = "En esta sala no puede entrar este Usuario"
                        return HttpResponse(json.dumps(response_data), content_type="application/json")

                else:
                    response_data = {}
                    response_data['result'] = 403
                    response_data['Error'] = "El usuario no tiene permisos"
                    return HttpResponse(json.dumps(response_data), content_type="application/json")


            else:
                response_data = {}
                response_data['result'] = 401
                response_data['Error'] = "El usuario esta desactivado"
                return HttpResponse(json.dumps(response_data), content_type="application/json")


        except Usuario.DoesNotExist:
            response_data = {}
            response_data['result'] = 401
            response_data['Error'] = "Usuario no existe"
            return HttpResponse(json.dumps(response_data), content_type="application/json")



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
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        # Comprobar si existe el imei
        try:
            consulta = Sala.objects.get(Hash=mensajeDesencriptado)
            # Comprobar que esta activa la sala y sino la activo

            response_data = {}
            response_data['result'] = 200
            response_data['IdSala'] = consulta.Id_Sala
            response_data['Dependencia']=consulta.Dependencia
            response_data['Plano'] = base64.encodestring(open(consulta.Plano.path, 'rb').read()).decode('ascii')
            if consulta.Activo:
                return HttpResponse(json.dumps(response_data), content_type="application/json")

            else:
                consulta.Activo = True
                consulta.save()
                return HttpResponse(json.dumps(response_data), content_type="application/json")

        except Sala.DoesNotExist:
            response_data = {}
            response_data['result'] = 404
            response_data['Error'] = "Imei no existe en la base de datos"
            return HttpResponse(json.dumps(response_data), content_type="application/json")