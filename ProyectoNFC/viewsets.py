from django.http import  JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .models import Registro,Usuario,Sala
from .serializer import RegistroSerializer,UsuarioSerializer,SalaSerializer


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
        serializer = UsuarioSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def SalaViewSet(request):

    if request.method == 'GET':
        query = Sala.objects.all()
        serializer = SalaSerializer(query, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SalaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
