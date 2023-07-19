from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .serializers import ComentariosSerializer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from .models import Comentarios 

@csrf_exempt
def crearComentario(request):
    if request.method == 'POST':
        datos = JSONParser().parse(request)
        comentario_serializer = ComentariosSerializer(data=datos)
        if comentario_serializer.is_valid():
            comentario_serializer.save()
            return JsonResponse("Guardado Exitosamente", safe=False)
        return JsonResponse("Error al guardar", safe=False)
    

@csrf_exempt
def obtenerComentario(request):
    if request.method == 'GET':
        comentarios = Comentarios.objects.all().order_by('-fechaHora')
        datosComenatrios = list(comentarios.values())
        print(comentarios)
        return JsonResponse(datosComenatrios, safe=False)
        


@csrf_exempt
def comentarioActualizar(request, id=0):
    if request.method == 'PUT':
        comentarios_data = JSONParser().parse(request)
        comentarios = Comentarios.objects.get(id=id)
        comentarios_serializer = ComentariosSerializer(comentarios, data=comentarios_data)
        if comentarios_serializer.is_valid():
            comentarios_serializer.save()
            return JsonResponse("Actualizado Exitosamente", safe=False)
        return JsonResponse("Failed to Update")
    

@csrf_exempt
def comentarioEliminar(request, id=0):
    if request.method == 'DELETE':
        comentarios = Comentarios.objects.get(id=id)
        comentarios.delete()
        return JsonResponse("Eliminado Exitosamente", safe=False)