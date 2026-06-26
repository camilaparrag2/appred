"""
Formularios para la aplicacion FeedPlan.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MediaPost, AgendaItem


class RegisterForm(UserCreationForm):
    """
    Formulario de registro de usuario con email requerido.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class MediaUploadForm(forms.ModelForm):
    """
    Formulario para subir imagenes al feed.
    """
    class Meta:
        model = MediaPost
        fields = ['image']


class AgendaItemForm(forms.ModelForm):
    """
    Formulario para crear/editar un item de la agenda semanal.
    """
    class Meta:
        model = AgendaItem
        fields = ['title', 'post_type', 'day', 'time', 'notes', 'images']
        widgets = {
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
            'post_type': forms.Select(attrs={'class': 'form-input'}),
            'day': forms.Select(attrs={'class': 'form-input'}),
            'images': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'title': 'Titulo del post',
            'post_type': 'Tipo de contenido',
            'day': 'Dia de la semana',
            'time': 'Hora (opcional)',
            'notes': 'Notas (opcional)',
            'images': 'Selecciona las imagenes',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Ej: Promocion verano'})
        self.fields['time'].widget.attrs.update({'class': 'form-input'})
