from django.contrib import admin


# Register your models here.

from .models import PerfilUsuario, Tarea, ComentarioTarea, Etiqueta

admin.site.register(PerfilUsuario)
admin.site.register(Tarea)
admin.site.register(ComentarioTarea)
admin.site.register(Etiqueta)