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
        'placeholder':'Ingrese una nueva contraseña',
        'class':'form-control',
        'autocomplete':'off'
    }))

    confirmPassword=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Repita la contraseña',
        'class':'form-control',
        'autocomplete':'off'
    }))

    def clean(self):
        cleaned=super().clean()
        password=cleaned['password']
        confirmPassword=cleaned['password']
        if password != confirmPassword:
            raise forms.ValidationError('Las contraseñas deben ser iguales')
        return cleaned
