from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Modelo para representar una tarea individual
class Tarea(models.Model):
    VISIBILIDAD_CHOICES = [
        ('privado', 'Privado'),
        ('publico', 'Público'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tareas')
    titulo = models.CharField(max_length=200, verbose_name='Título')
    descripcion = models.TextField(verbose_name='Descripción', null=True, blank=True)
    fecha = models.DateField(verbose_name='Fecha de la tarea')
    hora = models.TimeField(verbose_name='Hora de la tarea', null=True, blank=True)
    visibilidad = models.CharField(max_length=10, choices=VISIBILIDAD_CHOICES, default='privado')
    creada_en = models.DateTimeField(auto_now_add=True)
    actualizada_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"


# Modelo para permitir a los usuarios clonar rutinas públicas
class RutinaClonada(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rutinas_clonadas')
    tarea_original = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='clones')
    fecha_clonacion = models.DateTimeField(auto_now_add=True)
    modificada = models.BooleanField(default=False)

    def __str__(self):
        return f"Clon de {self.tarea_original.titulo} por {self.usuario.username}"
