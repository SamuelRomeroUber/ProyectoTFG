from django.urls import path
from . import views
from .views import *

urlpatterns = [
path('', home, name='home'),
path('registro/', RegistroView.as_view(), name='registro'),
path('perfil_usuario/', perfil_usuario, name='perfil_usuario'),
path('foro/', foro, name='foro'),

path('tarea/crear_tarea/', CrearTarea.as_view(), name='crear_tarea'),
path('tarea/listar_tareas/', ListarTarea.as_view(), name='listar_tareas'),
path('tarea/editar_tarea/<int:pk>/', EditarTarea.as_view(), name='editar_tarea'),
path('tarea/tarea_confirm_delete/<int:pk>/', BorrarTarea.as_view(), name='borrar_tarea'),
path('tarea/detalle_tarea/<int:pk>/', DetalleTarea.as_view(), name='detalle_tarea'),

path('tarea/marcar_completada/<int:pk>/', MarcarTareaCompletada.as_view(), name='marcar_tarea_completada'),

path('tarea/copiar_tarea/<int:pk_original>/', CopiarTarea, name='copiar_tarea'),
]