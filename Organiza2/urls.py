from django.urls import path
from . import views
from .views import RegistroView

urlpatterns = [
path('', views.home, name='home'),
path('registro/', RegistroView.as_view(), name='registro'),
path('perfil_usuario/', views.perfil_usuario, name='perfil_usuario'),

path('tarea/crear_tarea/', views.CrearTarea.as_view(), name='crear_tarea'),
]