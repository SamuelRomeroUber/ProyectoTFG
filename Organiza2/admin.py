from django.contrib import admin


# Register your models here.

from .models import PerfilUsuario, Tarea, ComentarioTarea

admin.site.register(PerfilUsuario)
admin.site.register(Tarea)
admin.site.register(ComentarioTarea)