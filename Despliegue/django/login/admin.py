from django.contrib import admin
from .models import Usuario

# Definir un administrador para personalizar la vista del modelo
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'contrasena')  # Opcional: puedes elegir qué campos mostrar en la lista
    search_fields = ('usuario',)  # Permite buscar por el campo 'usuario'
    
admin.site.register(Usuario, UsuarioAdmin)
