from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Tarea(models.Model):
    # Opciones para el estado de la tarea
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En progreso'),
        ('completada', 'Completada'),
    ]
    
    # Opciones para la visibilidad de la tarea
    VISIBILIDAD_CHOICES = [
        ('privada', 'Privada'),
        ('publica', 'Pública'),
    ]
    
    # Campos principales
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tareas')
    titulo = models.CharField(max_length=200, verbose_name='Título')
    descripcion = models.TextField(verbose_name='Descripción', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    fecha_vencimiento = models.DateTimeField(verbose_name='Fecha de vencimiento', blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente', verbose_name='Estado')
    visibilidad = models.CharField(max_length=20, choices=VISIBILIDAD_CHOICES, default='privada', verbose_name='Visibilidad')
    completada = models.BooleanField(default=False, verbose_name='Completada')
    fecha_completada = models.DateTimeField(blank=True, null=True, verbose_name='Fecha de completación')
    
    # Campos adicionales
    etiqueta = models.CharField(max_length=50, blank=True, null=True, verbose_name='Etiqueta')
    prioridad = models.PositiveIntegerField(default=1, verbose_name='Prioridad (1-5)', choices=[(i, str(i)) for i in range(1, 6)])
    
    class Meta:
        ordering = ['-prioridad', 'fecha_vencimiento']
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
    
    def __str__(self):
        return f"{self.titulo} - {self.get_estado_display()}"
    
    def save(self, *args, **kwargs):
        # Actualizar fecha_completada si la tarea se marca como completada
        if self.completada and not self.fecha_completada:
            self.fecha_completada = timezone.now()
        elif not self.completada and self.fecha_completada:
            self.fecha_completada = None
        super().save(*args, **kwargs)

class ComentarioTarea(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField(verbose_name='Comentario')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
    
    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.tarea.titulo}"

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Avatar')
    bio = models.TextField(blank=True, null=True, verbose_name='Biografía')
    fecha_nacimiento = models.DateField(blank=True, null=True, verbose_name='Fecha de nacimiento')
    ubicacion = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ubicación')
    
    def __str__(self):
        return f"Perfil de {self.usuario.username}"