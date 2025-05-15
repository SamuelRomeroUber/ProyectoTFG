from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# El modelo Etiqueta debe estar definido ANTES que Tarea si lo refieres directamente,
# o puedes usar una cadena 'Etiqueta' en el ForeignKey.
class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name='Nombre de la etiqueta')
    
    def __str__(self):
        return self.nombre

class Tarea(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En progreso'),
        ('completada', 'Completada'),
    ]
    VISIBILIDAD_CHOICES = [
        ('privada', 'Privada'),
        ('publica', 'Pública'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tareas')
    titulo = models.CharField(max_length=200, verbose_name='Título')
    descripcion = models.TextField(verbose_name='Descripción', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    fecha_vencimiento = models.DateTimeField(verbose_name='Fecha de vencimiento', blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente', verbose_name='Estado')
    visibilidad = models.CharField(max_length=20, choices=VISIBILIDAD_CHOICES, default='privada', verbose_name='Visibilidad')
    completada = models.BooleanField(default=False, verbose_name='Completada')
    fecha_completada = models.DateTimeField(blank=True, null=True, verbose_name='Fecha de completación')
    
    # --- MODIFICACIÓN AQUÍ ---
    etiqueta = models.ForeignKey(
        Etiqueta, 
        on_delete=models.SET_NULL, # O models.PROTECT, o lo que prefieras
        null=True, 
        blank=True, 
        verbose_name='Etiqueta'
    )
    # --- FIN MODIFICACIÓN ---
    
    prioridad = models.PositiveIntegerField(default=1, verbose_name='Prioridad (1-5)', choices=[(i, str(i)) for i in range(1, 6)])
    
    class Meta:
        ordering = ['-prioridad', 'fecha_vencimiento']
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
    
    def __str__(self):
        return f"{self.titulo} - {self.get_estado_display()}"
    
    def save(self, *args, **kwargs):
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