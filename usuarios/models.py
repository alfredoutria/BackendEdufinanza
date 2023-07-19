from django.db import models

class Usuarios(models.Model):
      nombre = models.CharField(max_length=30, default='')
      email = models.CharField(max_length=100)
      password = models.CharField(max_length=100)
      codigo = models.IntegerField(null=True, blank=True)

