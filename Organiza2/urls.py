from django.urls import path
from . import views
from .views import RegistroView

urlpatterns = [
path('', views.home, name='home'),
path('registro/', RegistroView.as_view(), name='registro'),
path('perfil_usuario/', views.perfil_usuario, name='perfil_usuario'),

path('tarea/crear_tarea/', views.CrearTarea.as_view(), name='crear_tarea'),
path('tarea/listar_tareas/', views.ListarTarea.as_view(), name='listar_tareas'),
path('tarea/editar_tarea/<int:pk>/', views.EditarTarea.as_view(), name='editar_tarea'),
path('tarea/tarea_confirm_delete/<int:pk>/', views.BorrarTarea.as_view(), name='borrar_tarea'),
path('tarea/detalle_tarea/<int:pk>/', views.DetalleTarea.as_view(), name='detalle_tarea')
]