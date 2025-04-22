from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import DatosImagen, Alimento
from hdfs import InsecureClient
from django.http import HttpResponse
from django.contrib import messages  
from django.utils.dateparse import parse_date
from datetime import datetime

# import jwt  # aniadir al requirements.txt

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('viewLogin')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})

def home(request):
    return render(request, 'home.html')


@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('bienvenida')
    
@login_required
def bienvenida(request):
    return render(request, 'bienvenida.html')

@login_required
def cuadro2(request):
    return render(request, 'cuadro2.html')

@login_required
def cuadro3(request):
    return render(request, 'cuadro3.html')

@login_required
def cuadro4(request):
    return render(request, 'cuadro4.html')

@login_required
def cuadro5(request):
    return render(request, 'cuadro5.html')


@login_required
def fotos(request):
    # Obtener nombres de imágenes desde MongoDB
    nombres_imagenes = DatosImagen.objects.values_list("nombre", flat=True)
    return render(request, "fotos.html", {"imagenes": nombres_imagenes})

@login_required
def proxy_imagen(request, nombre_imagen):
    # Cliente HDFS (ajusta según tu configuración)
    client = InsecureClient('http://namenode:50070', user='hadoop')  # Usa IP si hay problemas DNS
    
    try:
        # Leer imagen desde HDFS
        with client.read(f"/ondaakin/imagenes/{nombre_imagen}") as reader:
            content = reader.read()
            return HttpResponse(content, content_type="image/png")
    
    except Exception as e:
        return HttpResponse(f"Error al cargar la imagen: {str(e)}", status=404)


@login_required
def foto_detalle(request, nombre):

    # Obtener datos de MongoDB para llenar formulario
    imagen = get_object_or_404(DatosImagen, nombre=nombre)
    alimentos= Alimento.objects.all()

    # recibir formulario
    cambios = []
    if request.method == 'POST':                
        # Procesar cada campo del formulario
        for i in range(len(imagen.deteccion)):
            field_name = f'detec_{i}'
            nuevo_alimento = request.POST.get(field_name)
            
            # Comparar con el valor actual (solo si hay cambios)
            if nuevo_alimento and nuevo_alimento != imagen.deteccion[i][0]:
                cambios.append(f"Cambiado {imagen.deteccion[i][0]} → {nuevo_alimento}")
                # Actualizar el valor en la detección
                imagen.deteccion[i][0] = nuevo_alimento
            
        # Guardar los cambios en MongoDB 
        if cambios:
            imagen.save()  # guardar cambios en mongo
        
        return redirect('fotos')  # Redirige para evitar reenvío del formulario    
    
    # Pasar el objeto completo al contexto
    contexto = {'imagen': imagen ,
                'alimentos': alimentos,}

    return render(request, 'foto_detalle.html',contexto)


