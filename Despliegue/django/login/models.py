from django.contrib.auth.hashers import make_password
from djongo import models

class Usuario(models.Model):
    _id = models.ObjectIdField()  # Asegura que Django reconozca el campo _id de MongoDB
    usuario = models.CharField(max_length=100)
    contrasena = models.CharField(max_length=255)  # Aumentar el tamaño para el hash de la contraseña

    class Meta:
        db_table = "usuarios"

    def __str__(self):
        return self.usuario

    # Método para establecer la contraseña de forma segura (cifrada)
    def set_contrasena(self, raw_contrasena):
        self.contrasena = make_password(raw_contrasena)

    # Método para comprobar la contraseña
    def check_contrasena(self, raw_contrasena):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_contrasena, self.contrasena)

class DatosImagen(models.Model):
    nombre = models.CharField(max_length=100)
    deteccion = models.JSONField()  # Lista que contiene un número y otra lista
    peso = models.FloatField()
    fecha_adquisicion = models.DateTimeField()
    fecha_procesado = models.DateTimeField()

    class Meta:
        db_table = "datosImagen"  # Nombre de la colección en MongoDB
class Alimento(models.Model):
    id_mongo = models.AutoField(primary_key=True, db_column='_id') 
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = "alimentos"  
