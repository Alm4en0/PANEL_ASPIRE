from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    dni = models.CharField(max_length=8, unique=True)  
    celular = models.CharField(max_length=9, blank=False, null=False) 
    foto_perfil = models.ImageField(upload_to='foto_perfil/')
    fecha_registro = models.DateTimeField(auto_now_add=True)
