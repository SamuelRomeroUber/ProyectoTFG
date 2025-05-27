from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views import View
from django.db.models import Q

from Organiza2.forms import TareaForm
from .models import PerfilUsuario, Tarea, Etiqueta
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib import messages

from Organiza2 import models

# Vista principal
def home(request):
    return render(request, 'plantillas/index.html')

# Vista de perfil
@login_required
def perfil_usuario(request):
    # Se ordena para mostrar las no completadas primero, luego por prioridad y fecha
    tareas_usuario = Tarea.objects.filter(usuario=request.user).order_by('completada', '-prioridad', 'fecha_vencimiento')
    contexto = {
        'tareas': tareas_usuario
    }
    return render(request, 'plantillas/user/perfil_usuario.html', contexto)

# Vista para el foro
@login_required
def foro(request):
    # Obtener todas las tareas que son públicas
    tareas_publicas = Tarea.objects.filter(visibilidad='publica').order_by('-fecha_creacion')
    contexto = {
        'tareas_publicas': tareas_publicas
    }
    return render(request, 'plantillas/foro/foro.html', contexto)

# Vista de registro
class RegistroView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/registro.html'
    success_url = reverse_lazy('login')

# Vistas CRUD para Tareas
class CrearTarea(LoginRequiredMixin, CreateView):
    model= Tarea
    template_name= 'plantillas/tarea/crear_tarea.html'
    form_class=TareaForm
    success_url = reverse_lazy("perfil_usuario")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        return super().form_valid(form)
    
class ListarTarea(LoginRequiredMixin, ListView):
    model = Tarea
    template_name = 'plantillas/tarea/listar_tareas.html'

    def get_queryset(self):
        # Ordenar por no completadas primero, luego por fecha de creación
        return Tarea.objects.filter(usuario=self.request.user).order_by('completada', 'fecha_creacion')
    
class EditarTarea(LoginRequiredMixin, UpdateView):
    model = Tarea
    template_name = 'plantillas/tarea/editar_tarea.html'
    form_class = TareaForm
    success_url = reverse_lazy("perfil_usuario")

    def get_queryset(self): # Asegurar que solo el dueño pueda editar
        return Tarea.objects.filter(usuario=self.request.user)

    def get_form_kwargs(self): # Pasar el usuario al formulario
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class BorrarTarea(LoginRequiredMixin, DeleteView):
    model = Tarea
    template_name = 'plantillas/tarea/tarea_confirm_delete.html'
    success_url = reverse_lazy("perfil_usuario")

    def get_queryset(self): # Asegurar que solo el dueño pueda borrar
        return Tarea.objects.filter(usuario=self.request.user)

class DetalleTarea(LoginRequiredMixin, DetailView):
    model = Tarea
    template_name = 'plantillas/tarea/detalle_tarea.html'
    context_object_name = 'tarea'

    def get_queryset(self):
        # Permitir ver tareas propias o públicas
        return Tarea.objects.filter(
            Q(usuario=self.request.user) | Q(visibilidad='publica')
        ).distinct()

class MarcarTareaCompletada(LoginRequiredMixin, View):
    def post(self, request, pk):
        tarea = get_object_or_404(Tarea, pk=pk)
        
        # Verificar que el usuario actual es el dueño de la tarea
        if tarea.usuario != request.user:
            return HttpResponseForbidden("No tienes permiso para modificar esta tarea.")
            
        if not tarea.completada:
            tarea.completada = True
            tarea.estado = 'completada' # Me aseguro que el estado también cambie
        else:
            tarea.completada = False
            tarea.estado = 'pendiente'
        
        tarea.save()
        return redirect('perfil_usuario')
    
@login_required
def CopiarTarea(request, pk_original):
    if request.method == 'POST':
        tarea_original = get_object_or_404(Tarea, pk=pk_original, visibilidad='publica')

        nueva_tarea = Tarea()
        nueva_tarea.usuario = request.user # Asignar al usuario actual

        nueva_tarea.titulo = f"{tarea_original.titulo} (Copia)"
        nueva_tarea.descripcion = tarea_original.descripcion
        nueva_tarea.estado = 'pendiente'
        nueva_tarea.visibilidad = 'privada'
        nueva_tarea.prioridad = tarea_original.prioridad
        
        if tarea_original.etiqueta:
            nueva_tarea.etiqueta = tarea_original.etiqueta
        try:
            nueva_tarea.save()
            messages.success(request, f"Tarea '{tarea_original.titulo}' copiada a tu perfil.")
        except Exception as e:
            messages.error(request, f"Error al copiar la tarea: {e}")
            return redirect('foro')
        return redirect('perfil_usuario') 
    else:
        return redirect('foro')