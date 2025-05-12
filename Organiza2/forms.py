from django import forms
from .models import Tarea, Etiqueta
from django.contrib.auth.models import User
from django.utils import timezone

class TareaForm(forms.ModelForm):
    etiqueta = forms.ModelChoiceField(
        queryset=Etiqueta.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'data-placeholder': 'Selecciona o crea una etiqueta',
        }),
        label='Etiqueta',
    )
    class Meta:
        model = Tarea
        fields = [
            'titulo',
            'descripcion',
            'fecha_vencimiento',
            'estado',
            'visibilidad',
            'completada',
            'etiqueta',
            'prioridad',
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título de la tarea'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción detallada',
                'rows': 3
            }),
            'fecha_vencimiento': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'visibilidad': forms.Select(attrs={
                'class': 'form-select'
            }),
            'completada': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'etiqueta': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Selecciona o escribe una etiqueta',
            }),
            'prioridad': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'fecha_vencimiento': 'Fecha de vencimiento',
            'estado': 'Estado',
            'visibilidad': 'Visibilidad',
            'completada': '¿Completada?',
            'etiqueta': 'Etiqueta',
            'prioridad': 'Prioridad',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TareaForm, self).__init__(*args, **kwargs)
        
        # Personalizar las opciones de prioridad
        self.fields['prioridad'].choices = [(i, str(i)) for i in range(1, 6)]
        
        # Si se proporciona un usuario, establecerlo como usuario de la tarea
        if user:
            self.instance.usuario = user

    def clean_etiqueta(self):
        etiqueta = self.cleaned_data.get('etiqueta')
        if isinstance(etiqueta, str):
            etiqueta, created = Etiqueta.objects.get_or_create(nombre=etiqueta)
        return etiqueta

    def clean_fecha_vencimiento(self):
        fecha_vencimiento = self.cleaned_data.get('fecha_vencimiento')
        if fecha_vencimiento and fecha_vencimiento < timezone.now():
            raise forms.ValidationError("La fecha de vencimiento no puede ser en el pasado.")
        return fecha_vencimiento