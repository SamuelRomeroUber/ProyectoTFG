from django import forms
from .models import Tarea, Etiqueta
from django.utils import timezone
from django.forms import ModelChoiceField, ValidationError

# --- CreatableModelChoiceField (sin cambios) ---
class CreatableModelChoiceField(ModelChoiceField):
    def clean(self, value):
        if value in self.empty_values:
            return None
        try:
            obj = self.queryset.get(**{self.to_field_name or 'pk': value})
            return obj
        except (ValueError, TypeError, self.queryset.model.DoesNotExist):
            if isinstance(value, str):
                normalized_value = value.strip()
                if not normalized_value:
                    return None
                try:
                    obj, created = self.queryset.get_or_create(
                        nombre=normalized_value,
                        defaults={'nombre': normalized_value}
                    )
                    return obj
                except Exception as e:
                    raise ValidationError(f"No se pudo crear o encontrar la etiqueta: '{value}'. Verifique que el nombre sea único.")
            else:
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
            'estado',           # Mantenemos estado
            'visibilidad',
            # 'completada',     # Eliminamos este campo del formulario
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
            'estado': forms.Select(attrs={  # El widget se mantiene, pero ajustaremos choices
                'class': 'form-select'
            }),
            'visibilidad': forms.Select(attrs={
                'class': 'form-select'
            }),
            # El widget para 'completada' se elimina ya que el campo no está
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
        
        # Ajustar las opciones para el campo 'estado'
        # Excluimos la opción 'completada' del formulario
        estado_choices = [choice for choice in Tarea.ESTADO_CHOICES if choice[0] != 'completada']
        self.fields['estado'].choices = estado_choices
        
        # Si la tarea ya existe y está completada, mantenemos el estado 'completada'
        # pero el select no lo mostrará como opción editable si no está entre las choices.
        # Esto es más para la edición, para creación no importa.
        if self.instance and self.instance.pk and self.instance.estado == 'completada':
             # Si quieres que aparezca "Completada" si YA está completada (solo visual, no seleccionable)
             # podrías añadirlo dinámicamente, o simplemente dejar que el modelo maneje esto.
             # Por ahora, si está completada, el select mostrará el primer estado disponible o vacío.
             # Lo ideal es que si está completada, no se edite el estado desde aquí directamente.
             # La lógica de completar se hará con el tick.
             pass # Dejamos que el valor inicial se establezca, pero 'completada' no será una opción nueva a elegir

        self.fields['prioridad'].choices = [(i, str(i)) for i in range(1, 6)]
        
        if user:
            self.instance.usuario = user

    def clean_fecha_vencimiento(self):
        fecha_vencimiento = self.cleaned_data.get('fecha_vencimiento')
        return fecha_vencimiento