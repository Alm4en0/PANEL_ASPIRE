from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    dni = models.CharField(max_length=8, unique=True)  
    celular = models.CharField(max_length=15, blank=False, null=False) 
    foto_perfil = models.ImageField(upload_to='foto_perfil/', null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    genero = models.CharField(max_length=15,blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk is None:  # Si es un nuevo objeto
            self.set_password(self.password)
        else:
            user = CustomUser.objects.get(pk=self.pk)
            if user.password != self.password:
                self.set_password(self.password)
        super().save(*args, **kwargs)
