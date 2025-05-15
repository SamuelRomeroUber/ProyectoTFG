from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from Organiza2.forms import TareaForm
from .models import PerfilUsuario, Tarea
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


# Esta es la vista principal de la aplicación
def home(request):
    return render(request, 'plantillas/index.html')

# Vista para mostrar el perfil del usuario cuando está logueado
@login_required
def perfil_usuario(request):
    return render(request, 'plantillas/user/perfil_usuario.html')

# Vista para mostrar el foro
@login_required
def foro(request):
    return render(request, 'plantillas/foro/foro.html')

# Vista para el registro de un nuevo usuario
class RegistroView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/registro.html'
    success_url = reverse_lazy('login')

# Vista para añadir nueva tarea
class CrearTarea(CreateView):
    model= Tarea
    template_name= 'plantillas/tarea/crear_tarea.html'
    form_class=TareaForm
    success_url = reverse_lazy("perfil_usuario")


    def form_valid(self, form):
        form.instance.usuario = self.request.user # Asigna el usuario actual a la tarea
        return super().form_valid(form)
    
class ListarTarea(ListView):
    model = Tarea
    template_name = 'plantillas/tarea/listar_tareas.html'

    # Aquí se filtran las tareas por la fecha de creación
    def get_queryset(self):
        return Tarea.objects.filter(usuario=self.request.user).order_by('fecha_creacion')
    
class EditarTarea(UpdateView):
    model = Tarea
    template_name = 'plantillas/tarea/editar_tarea.html'
    form_class = TareaForm
    success_url = reverse_lazy("listar_tareas")

class BorrarTarea(DeleteView):
    model = Tarea
    template_name = 'plantillas/tarea/tarea_confirm_delete.html'
    success_url = reverse_lazy("listar_tareas")

class DetalleTarea(DetailView):
    model = Tarea
    template_name = 'plantillas/tarea/detalle_tarea.html'
    context_object_name = 'tarea'