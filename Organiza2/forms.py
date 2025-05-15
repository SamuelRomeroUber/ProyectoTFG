from django import forms
from .models import Tarea, Etiqueta
from django.utils import timezone
from django.forms import ModelChoiceField, ValidationError # Asegúrate de importar ValidationError

# --- NUEVO CAMPO PERSONALIZADO ---
class CreatableModelChoiceField(ModelChoiceField):
    def clean(self, value):
        # value es la cadena raw de la subida del formulario.
        # TomSelect envía el PK para ítems existentes, o el texto para ítems nuevos.
        if value in self.empty_values:
            return None

        # Intenta encontrar por PK primero (para etiquetas existentes seleccionadas)
        try:
            obj = self.queryset.get(**{self.to_field_name or 'pk': value})
            return obj
        except (ValueError, TypeError, self.queryset.model.DoesNotExist):
            # Si no es un PK válido o no se encuentra por PK, asume que es un nombre nuevo.
            if isinstance(value, str):
                # Normaliza el valor (ej. quitar espacios, convertir a minúsculas si es necesario)
                normalized_value = value.strip()
                if not normalized_value: # Manejar cadena vacía después de strip
                    return None
                
                # Intenta obtener o crear la etiqueta por su nombre
                # Asumimos que el campo para crear/buscar es 'nombre'
                try:
                    obj, created = self.queryset.get_or_create(
                        nombre=normalized_value, 
                        defaults={'nombre': normalized_value} # Asegura que 'nombre' se guarde
                    )
                    return obj
                except Exception as e:
                    # Esto podría capturar IntegrityError si 'nombre' no es único y hay un conflicto,
                    # o otros errores de base de datos.
                    # Considera loggear el error 'e' para depuración.
                    raise ValidationError(f"No se pudo crear o encontrar la etiqueta: '{value}'. Verifique que el nombre sea único.")
            else:
                # Este caso no debería alcanzarse si TomSelect envía cadenas.
                raise ValidationError(self.error_messages['invalid_choice'], code='invalid_choice')
# --- FIN NUEVO CAMPO PERSONALIZADO ---

class TareaForm(forms.ModelForm):
    # --- MODIFICACIÓN AQUÍ ---
    etiqueta = CreatableModelChoiceField(
        queryset=Etiqueta.objects.all(),
        required=False,
        widget=forms.Select(attrs={  # TomSelect mejorará este <select>
            'class': 'form-select', # Mantenemos para estilos generales si los hay
            'id': 'id_etiqueta_tomselect', # ID explícito para el JS de TomSelect
            # TomSelect recogerá el placeholder del <script>
        }),
        label='Etiqueta',
        help_text="Selecciona una etiqueta existente o escribe un nuevo nombre para crearla."
    )
    # --- FIN MODIFICACIÓN ---

    class Meta:
        model = Tarea
        fields = [
            'titulo',
            'descripcion',
            'fecha_vencimiento',
            'estado',
            'visibilidad',
            'completada',
            'etiqueta', # Ahora 'etiqueta' usará nuestro campo personalizado
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
            # El widget para 'etiqueta' se define arriba
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
            # 'etiqueta': 'Etiqueta', # Definido en el campo mismo
            'prioridad': 'Prioridad',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TareaForm, self).__init__(*args, **kwargs)
        
        self.fields['prioridad'].choices = [(i, str(i)) for i in range(1, 6)]
        
        if user:
            self.instance.usuario = user

    # Ya no necesitas clean_etiqueta aquí porque CreatableModelChoiceField lo maneja
    # def clean_etiqueta(self):
    #     ...

    def clean_fecha_vencimiento(self):
        fecha_vencimiento = self.cleaned_data.get('fecha_vencimiento')
        # Permitir fechas de vencimiento en el pasado si es necesario, o mantener la validación
        # if fecha_vencimiento and fecha_vencimiento < timezone.now():
        #     raise forms.ValidationError("La fecha de vencimiento no puede ser en el pasado.")
        return fecha_vencimiento