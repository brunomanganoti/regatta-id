from django.db import models
from .usuario import Usuario

class EventoCritico(models.Model):
    usuario     = models.ForeignKey(Usuario, on_delete=models.SET_NULL,
                                    null=True, blank=True, related_name="eventos_criticos")
    tipo_evento = models.CharField(max_length=255)
    descricao   = models.TextField(blank=True, null=True)
    data_evento = models.DateTimeField(auto_now_add=True)
    
