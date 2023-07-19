from django.db import models

class Comentarios(models.Model):
      fechaHora = models.DateTimeField(auto_now_add=True)
      usuario = models.CharField(max_length=100)
      comentario = models.CharField(max_length=1000)
