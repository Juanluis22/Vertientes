from django.forms import *
from django import forms
from nucleo.models import comunidad, vertiente
from user.models import User


class TestForm(Form):
    comunidad=ModelChoiceField(
        queryset=comunidad.objects.all(),
        widget=Select(
            attrs={
                'class':'form-control'

    }))
    vertiente=ModelChoiceField(
        queryset=vertiente.objects.none(),
        widget=Select(
            attrs={
                'class':'form-control'

    }))


class ResetPasswordForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Ingrese username',
        'class':'form-control',
        'autocomplete':'off'
    }))

    def clean(self):
        cleaned=super().clean()
        if not User.objects.filter(username=cleaned['username']).exists:
            raise forms.ValidationError('El usuario no existe')
        return cleaned
    
    def get_user(self):
        username=self.cleaned_data.get('username')
        return User.objects.get(username=username)
    


class ChangePasswordForm(forms.Form):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'nueva contraseña',
        'class':'form-control',
        'autocomplete':'off'
    }))

    confirmPassword=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Repita la contraseña',
        'class':'form-control',
        'autocomplete':'off'
    }))

    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmPassword = cleaned_data.get('confirmPassword')

        if password and confirmPassword:
         if password != confirmPassword:
            self.add_error('confirmPassword', 'Las contraseñas deben ser igualess')
         else:
             self.success_message = "Su contraseña se ha cambiado correctamente."

        return cleaned_data

    

