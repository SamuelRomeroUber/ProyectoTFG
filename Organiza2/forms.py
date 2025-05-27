from django import forms
from .models import Tarea, Etiqueta
from django.utils import timezone
from django.forms import ModelChoiceField, ValidationError

class CreatableModelChoiceField(ModelChoiceField):
    def clean(self, value):
        # Si el valor está vacío (None, '', etc.), retorna None.
        if value in self.empty_values:
            return None
        try:
            # Intenta obtener el objeto del queryset usando el valor como clave primaria (o el campo especificado).
            obj = self.queryset.get(**{self.to_field_name or 'pk': value})
            return obj
        except (ValueError, TypeError, self.queryset.model.DoesNotExist):
            # Si no se puede encontrar el objeto (o el valor es inválido), verifica si el valor es un string.
            if isinstance(value, str):
                normalized_value = value.strip()  # Elimina espacios al inicio y final.
                if not normalized_value:
                    return None  # Si después de limpiar está vacío, retorna None.
                try:
                    # Intenta obtener o crear un objeto con el nombre normalizado.
                    obj, created = self.queryset.get_or_create(
                        nombre=normalized_value,
                        defaults={'nombre': normalized_value}
                    )
                    return obj
                except Exception as e:
                    # Si falla la creación, lanza un error de validación con un mensaje personalizado.
                    raise ValidationError(f"No se pudo crear o encontrar la etiqueta: '{value}'. Verifique que el nombre sea único.")
            else:
                # Si el valor no es string y no se encontró, lanza un error de validación estándar.
                raise ValidationError(self.error_messages['invalid_choice'], code='invalid_choice')

class TareaForm(forms.ModelForm):
    etiqueta = CreatableModelChoiceField(
        queryset=Etiqueta.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_etiqueta_tomselect',
        }),
        label='Etiqueta',
        help_text="Selecciona una etiqueta existente o escribe un nuevo nombre para crearla."
    )

    class Meta:
        model = Tarea
        fields = [
            'titulo',
            'descripcion',
            'fecha_vencimiento',
            'estado',
            'visibilidad',
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
            'prioridad': 'Prioridad',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TareaForm, self).__init__(*args, **kwargs)
        
        estado_choices = [choice for choice in Tarea.ESTADO_CHOICES if choice[0] != 'completada']
        self.fields['estado'].choices = estado_choices
        
        if self.instance and self.instance.pk and self.instance.estado == 'completada':
            pass #'completada' no será una opción nueva a elegir

        self.fields['prioridad'].choices = [(i, str(i)) for i in range(1, 6)]
        
        if user:
            self.instance.usuario = user

    def clean_fecha_vencimiento(self):
        fecha_vencimiento = self.cleaned_data.get('fecha_vencimiento')
        return fecha_vencimiento