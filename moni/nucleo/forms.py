from django.forms import *  # Importa todas las clases y funciones del módulo django.forms
from django import forms  # Importa el módulo forms de Django
from nucleo.models import comunidad, vertiente  # Importa los modelos comunidad y vertiente desde nucleo.models
from user.models import User  # Importa el modelo User desde user.models

class TestForm(Form):
    """
    Formulario de prueba que incluye campos para seleccionar una comunidad y una vertiente.
    """
    comunidad = ModelChoiceField(
        queryset=comunidad.objects.all(),  # Consulta para obtener todas las comunidades
        widget=Select(
            attrs={
                'class': 'form-control'  # Clase CSS para el campo de selección de comunidad
            }
        )
    )
    vertiente = ModelChoiceField(
        queryset=vertiente.objects.none(),  # Consulta vacía para las vertientes, se llenará dinámicamente
        widget=Select(
            attrs={
                'class': 'form-control'  # Clase CSS para el campo de selección de vertiente
            }
        )
    )

class ResetPasswordForm(forms.Form):
    """
    Formulario para restablecer la contraseña de un usuario.
    """
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ingrese username',  # Texto de marcador de posición
                'class': 'form-control',  # Clase CSS para el campo de entrada de texto
                'autocomplete': 'off'  # Desactiva el autocompletado del navegador
            }
        )
    )

    def clean(self):
        """
        Valida que el usuario exista en la base de datos.
        """
        cleaned = super().clean()
        if not User.objects.filter(username=cleaned['username']).exists():
            raise forms.ValidationError('El usuario no existe')  # Lanza un error si el usuario no existe
        return cleaned
    
    def get_user(self):
        """
        Obtiene el usuario basado en el nombre de usuario proporcionado.
        """
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)  # Devuelve el usuario correspondiente

class ChangePasswordForm(forms.Form):
    """
    Formulario para cambiar la contraseña de un usuario.
    """
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'nueva contraseña',  # Texto de marcador de posición
                'class': 'form-control',  # Clase CSS para el campo de entrada de contraseña
                'autocomplete': 'off'  # Desactiva el autocompletado del navegador
            }
        )
    )

    confirmPassword = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repita la contraseña',  # Texto de marcador de posición
                'class': 'form-control',  # Clase CSS para el campo de entrada de confirmación de contraseña
                'autocomplete': 'off'  # Desactiva el autocompletado del navegador
            }
        )
    )

    def clean(self):
        """
        Valida que las contraseñas coincidan.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmPassword = cleaned_data.get('confirmPassword')

        if password and confirmPassword:
            if password != confirmPassword:
                self.add_error('confirmPassword', 'Las contraseñas deben ser iguales')  # Agrega un error si las contraseñas no coinciden
            else:
                self.success_message = "Su contraseña se ha cambiado correctamente."  # Mensaje de éxito si las contraseñas coinciden

        return cleaned_data