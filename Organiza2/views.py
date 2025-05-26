from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views import View # Importar View
from django.db.models import Q  # Importar Q para consultas complejas

from Organiza2.forms import TareaForm
from .models import PerfilUsuario, Tarea # Asegúrate que Tarea esté importado
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from Organiza2 import models

# Vista principal (sin cambios)
def home(request):
    return render(request, 'plantillas/index.html')

# Vista de perfil (sin cambios)
@login_required
def perfil_usuario(request):
    # Ordenamos para mostrar las no completadas primero, luego por prioridad y fecha
    tareas_usuario = Tarea.objects.filter(usuario=request.user).order_by('completada', '-prioridad', 'fecha_vencimiento')
    contexto = {
        'tareas': tareas_usuario
    }
    return render(request, 'plantillas/user/perfil_usuario.html', contexto)

# Vista para el foro (MODIFICADA)
@login_required
def foro(request):
    # Obtener todas las tareas que son públicas
    tareas_publicas = Tarea.objects.filter(visibilidad='publica').order_by('-fecha_creacion')
    contexto = {
        'tareas_publicas': tareas_publicas
    }
    return render(request, 'plantillas/foro/foro.html', contexto)

# Vista de registro (sin cambios)
class RegistroView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/registro.html'
    success_url = reverse_lazy('login')

# Vistas CRUD para Tareas
class CrearTarea(LoginRequiredMixin, CreateView): # Añadir LoginRequiredMixin
    model= Tarea
    template_name= 'plantillas/tarea/crear_tarea.html'
    form_class=TareaForm
    success_url = reverse_lazy("perfil_usuario")

    def get_form_kwargs(self): # Pasar el usuario al formulario
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # El usuario ya se asigna en __init__ de TareaForm si se pasa por get_form_kwargs
        # form.instance.usuario = self.request.user 
        return super().form_valid(form)
    
class ListarTarea(LoginRequiredMixin, ListView): # Añadir LoginRequiredMixin
    model = Tarea
    template_name = 'plantillas/tarea/listar_tareas.html'

    def get_queryset(self):
        # Ordenar por no completadas primero, luego por fecha de creación
        return Tarea.objects.filter(usuario=self.request.user).order_by('completada', 'fecha_creacion')
    
class EditarTarea(LoginRequiredMixin, UpdateView): # Añadir LoginRequiredMixin
    model = Tarea
    template_name = 'plantillas/tarea/editar_tarea.html'
    form_class = TareaForm
    success_url = reverse_lazy("perfil_usuario") # Cambiado para mejor UX

    def get_queryset(self): # Asegurar que solo el dueño pueda editar
        return Tarea.objects.filter(usuario=self.request.user)

    def get_form_kwargs(self): # Pasar el usuario al formulario
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class BorrarTarea(LoginRequiredMixin, DeleteView): # Añadir LoginRequiredMixin
    model = Tarea
    template_name = 'plantillas/tarea/tarea_confirm_delete.html'
    success_url = reverse_lazy("perfil_usuario") # Cambiado para mejor UX

    def get_queryset(self): # Asegurar que solo el dueño pueda borrar
        return Tarea.objects.filter(usuario=self.request.user)

class DetalleTarea(LoginRequiredMixin, DetailView): # Añadir LoginRequiredMixin
    model = Tarea
    template_name = 'plantillas/tarea/detalle_tarea.html'
    context_object_name = 'tarea'

    def get_queryset(self):
        # Permitir ver tareas propias o públicas
        return Tarea.objects.filter(
            Q(usuario=self.request.user) | Q(visibilidad='publica')
        ).distinct()

# --- NUEVA VISTA PARA MARCAR TAREA COMO COMPLETADA ---
class MarcarTareaCompletadaView(LoginRequiredMixin, View):
    def post(self, request, pk):
        tarea = get_object_or_404(Tarea, pk=pk)
        
        # Verificar que el usuario actual es el dueño de la tarea
        if tarea.usuario != request.user:
            return HttpResponseForbidden("No tienes permiso para modificar esta tarea.")
            
        # Cambiar estado y booleano 'completada'
        if not tarea.completada:
            tarea.completada = True
            tarea.estado = 'completada' # Asegurarse que el estado también cambie
        # Si se quisiera implementar "desmarcar":
        else:
            tarea.completada = False
            tarea.estado = 'pendiente' # O el estado anterior si se guarda
        
        tarea.save() # El método save de Tarea se encarga de fecha_completada
        return redirect('perfil_usuario')

    def get(self, request, pk):
        # Redirigir si se accede por GET, ya que es una acción de modificación
        return redirect('perfil_usuario')