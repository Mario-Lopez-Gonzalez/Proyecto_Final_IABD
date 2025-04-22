"""OndAAkinG3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from login import views
from django.urls import include

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),   
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('bienvenida/', views.bienvenida, name='bienvenida'),
    path('cuadro2/', views.cuadro2, name='cuadro2'),
    path('cuadro3/', views.cuadro3, name='cuadro3'),
    path('cuadro4/', views.cuadro4, name='cuadro4'),
    path('cuadro5/', views.cuadro5, name='cuadro5'),
    path('rag/', include('rag.urls')),
    path('fotos/', views.fotos, name='fotos'),
    path('fotos/<str:nombre>/', views.foto_detalle, name='foto_detalle'),
    path('imagen/<str:nombre_imagen>/', views.proxy_imagen, name='proxy_imagen'),
] 

