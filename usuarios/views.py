from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from .serializers import UsuariosSerializer
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.contrib.auth import authenticate
from .models import Usuarios
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from dotenv import load_dotenv
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
import json
import jwt
import string
import random

load_dotenv()

def index(request):
    return HttpResponse('Desarrollado en Framework Django')


@csrf_exempt
def usuarioCrear(request):
    if request.method == 'POST':
        datos = JSONParser().parse(request)
        nombre = datos.get('nombre')
        emailUsuario = datos.get('email')
        clave = datos.get('password')
        claveEncriptada = make_password(clave)
        codigo = datos.get('codigo')
        
        verificarCorreo = Usuarios.objects.filter(email = emailUsuario).exists()
        verificarUsuario = Usuarios.objects.filter(nombre = nombre).exists()

        if not verificarCorreo:
            if not verificarUsuario:
             usuario = Usuarios(nombre = nombre, email = emailUsuario, password = claveEncriptada, codigo = codigo)
             usuario_serializer = UsuariosSerializer(data = datos)
             if usuario_serializer.is_valid():
               usuario.save()
               return JsonResponse("Guardado exitosamente", safe=False)
            return JsonResponse("Usuario ya existe", safe=False)
        return JsonResponse("Correo ya existe", safe=False)
    


@csrf_exempt
def usuarioRecuperar(request):
    if request.method == 'POST':
       datos = JSONParser().parse(request)
       emailUsuario = datos.get('email')
       verificarUsuario = Usuarios.objects.filter(email = emailUsuario).exists()

       if verificarUsuario:
          digitos = 4
          caracteres = string.digits
          codigoVerificacion = ''.join(random.choice(caracteres) for _ in range(digitos))
          BuscarusuarioEmail = Usuarios.objects.get(email = emailUsuario)
          BuscarusuarioEmail.codigo = codigoVerificacion
          BuscarusuarioEmail.save()

          message = Mail(
               from_email='mensaje.destinatario@outlook.com',
               to_emails= emailUsuario,
               subject= 'Código de recuperación de Edufinanzas',
               html_content=f'Tu código de recuperación es {codigoVerificacion}')
          try:
            sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
          except Exception as e:
            print(e.message)

          return JsonResponse("Enviado exitosamente", safe=False)
       return JsonResponse("Email no existe", safe=False)


@csrf_exempt
def ActualizarClave(request):
    if request.method == 'POST':
       datos = JSONParser().parse(request)
       email = datos.get('email')
       codigo = datos.get('codigo')
       clave = datos.get('password')
       verificarCodigo = Usuarios.objects.filter(codigo = codigo).exists()

       if(verificarCodigo):
         BuscarEmail =  Usuarios.objects.get(email = email)
         claveEncriptada = make_password(clave)
         BuscarEmail.password  = claveEncriptada
         BuscarEmail.save()
         return JsonResponse("Contraseña Guardada", safe=False)
       return  JsonResponse("El codigo no es valido", safe=False)      
 
    

@csrf_exempt
def obtenerUsuario(request):
    if request.method == 'GET':
        usuario = Usuarios.objects.all()
        usuario_serializer = UsuariosSerializer(usuario, many=True)
        return JsonResponse(usuario_serializer.data, safe=False)


@csrf_exempt
def usuarioActualizar(request, id=0):
    if request.method == 'PUT':
        usuario_data = JSONParser().parse(request)
        usuario = Usuarios.objects.get(id=id)
        usuario_serializer = UsuariosSerializer(usuario, data=usuario_data)
        if usuario_serializer.is_valid():
            usuario_serializer.save()
            return JsonResponse("Actualizado Exitosamente", safe=False)
        return JsonResponse("Failed to Update")


@csrf_exempt
def usuarioEliminar(request, id=0):
    if request.method == 'DELETE':
        usuario = Usuarios.objects.get(id=id)
        usuario.delete()
        return JsonResponse("Eliminado Exitosamente", safe=False)


@csrf_exempt
def login(request):
  if request.method == 'POST':
    try:
      datos = json.loads(request.body)
      email = datos.get('email')
      password = datos.get('password')

      try:
         usuario = Usuarios.objects.get(email=email)
         
         if usuario is not None:
          if check_password(password, usuario.password):
          
           # Autenticación exitosa, generar el token JWT
            header = {
             'email': usuario.email,
            }
            token = jwt.encode(header, settings.SECRET_KEY, algorithm='HS256')
            return JsonResponse({'token': token,'nombre': usuario.nombre})
          return JsonResponse('La contraseña no es valida', safe=False)
      except Usuarios.DoesNotExist:
         return JsonResponse('El correo no existe', safe=False) 
    except json.JSONDecodeError:
      return JsonResponse({'error': 'Datos JSON inválidos'}, status=400, safe=False)
  return JsonResponse({'error': 'Método no permitido'}, status=405, safe=False)


