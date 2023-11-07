from django.forms import *
from django.contrib.auth.forms import UserCreationForm
from nucleo.models import *
from user.models import User,Profile
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

class ComunidadForm(ModelForm):
    class Meta:
        model= comunidad
        fields='__all__'
        exclude=['vertientes']

class VertienteForm(ModelForm):
    class Meta:
        model= vertiente
        fields=['nombre','desc','ubicación','comunidad','latitud','longitud']
        
class KitForm(ModelForm):

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
    
    class Meta:
        model= kit
        fields = ['modelo', 'mac', 'is_active', 'comunidad', 'vertiente']


def validate_rut(value):
        value = value.replace('.', '')  # Elimina puntos
        value = value.replace('-', '')  # Elimina guiones
        
        if len(value)>9:
            raise ValidationError('RUT inválido, ingrese un RUT de 9 digitos maximo')

        if not value[:-1].isdigit() or value[-1].lower() not in '0123456789k':
            raise ValidationError('Rut inválido')
        
        
        




class UserForm(ModelForm):
    email = forms.CharField(validators=[validators.EmailValidator(message="El correo electrónico debe ser válido.")])
    confirmar_contraseña = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model= User
        fields=['username','first_name','last_name','email',
                'edad','gender','comunidad','password']
        labels={
            'username':'RUT',
            'first_name':'Nombre',
            'last_name':'Apellido',
            'email':'Correo electronico',
            'edad':'Rango de edad',
            'gender':'Género',
            'password':'Contraseña',
        }
        help_texts = {
            'username': '',
            'first_name': '',
            'last_name': '',
            'email': '',
            'edad': '',
            'password': '*Le recomendamos escribir una contraseña sencilla, como pueden ser, los últimos 4 digitos de su RUT.',
        }
        



        widgets={
            'username':TextInput( 
                attrs={
                    'class':'form-control',
                    'placeholder':'Escriba su rut con el formato: (203627904)'

                }
            ), 
            

            'first_name':TextInput( 
                attrs={
                    'class':'form-control',
                    'placeholder':'Pedro'

                }
            ),
            'last_name':TextInput( 
                attrs={
                    'class':'form-control',
                    'placeholder':'Muñoz'

                }
            ),
            'email':TextInput( 
                attrs={
                    'class':'form-control',
                    'placeholder':'Pedromuñoz@gmail.com'

                }
            ),
            'password':PasswordInput( 
                attrs={
                    'class':'form-control',
                    

                }
            ),
        }
    

    
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['comunidad'].required = True
        self.fields['username'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['edad'].required = True
        self.fields['email'].required = True
        self.fields['gender'].required = True
        self.fields['password'].required = True
    

    

    def clean_username(self):
        username = self.cleaned_data['username']
        validate_rut(username)  # Llama a la función de validación personalizada
        username = username.replace('.', '')  # Elimina puntos
        username = username.replace('-', '')  # Elimina guiones
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password")
        confirmar_contraseña = cleaned_data.get("confirmar_contraseña")

        if password1 != confirmar_contraseña:
            raise forms.ValidationError("Las contraseñas no coinciden")



    def save(self, commit=True):
        data = {}
        form = super()
        if form.is_valid():
            pwd = self.cleaned_data['password']
            u = form.save(commit=False)
            if u.pk is None:
                u.set_password(pwd)
                u.save()  # Save the user first to get a primary key (u.pk)
                
                # Create a Profile instance for the user
                profile = Profile(user=u, group_id=2)
                profile.save()
            else:
                user = User.objects.get(pk=u.pk)
                if user.password != pwd:
                    u.set_password(pwd)
                u.save()
        else:
            data['error'] = form.errors



class UpdateForm(ModelForm):
    ROLES = (
        (1, 'Usuario'),
        (2, 'Autoridad'),
        (3, 'Administrador')
    )
    email = forms.CharField(validators=[validators.EmailValidator(message="El correo electrónico debe ser válido.")])
    tipo = forms.ChoiceField(choices=ROLES, label='Rol')
    class Meta:
        model= User
        fields=['username','first_name','last_name','email',
                'edad','comunidad','tipo','is_active']
        labels={
            'username':'RUT',
            'first_name':'Nombre',
            'last_name':'Apellido',
            'email':'Correo electrónico',
            'edad':'Edad',
            'is_active':'Estado',
        }
        widgets={
            'username':TextInput( 
                attrs={
                    'class':'form-control',
                    'placeholder':'Escriba su rut con el formato: (203627904)'

                }
            ),
            'first_name':TextInput( 
                attrs={
                    'class':'form-control',
                    'placeholder':'Pedro'

                }
            ),
            'last_name':TextInput( 
                attrs={
                    'class':'form-control',
                    'placeholder':'Muñoz'

                }
            ),
            'email':TextInput( 
                attrs={
                    'class':'form-control',
                    'placeholder':'Pedromuñoz@gmail.com'

                }
            ),
            
            'tipo':TextInput( 
                attrs={
                    'class':'form-control',
                    

                }
            ),
            
        }


    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        self.fields['comunidad'].required = True
        self.fields['username'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['edad'].required = True
        self.fields['email'].required = True
        

    def clean_username(self):
        username = self.cleaned_data['username']
        validate_rut(username)  # Llama a la función de validación personalizada
        return username
    
    

class UpdateFormPerfil(ModelForm):
    
    email = forms.CharField(validators=[validators.EmailValidator(message="El correo electrónico debe ser válido.")])
    nueva_contraseña = forms.CharField(max_length=100)
    confirmar_contraseña = forms.CharField(max_length=100)
    class Meta:
        model= User
        fields=['username','first_name','last_name','email',
                'edad','comunidad']
        labels={
            'username':'RUT',
            'first_name':'Nombre',
            'last_name':'Apellido',
            'email':'Correo electrónico',
            'edad':'Edad',
            
        }
        widgets={
            'username':TextInput( 
                attrs={
                    'class':'form-control',
                    'placeholder':'Escriba su rut con el formato: (203627904)'

                }
            ),
            'first_name':TextInput( 
                attrs={
                    'class':'form-control',
                    'placeholder':'Pedro'

                }
            ),
            'last_name':TextInput( 
                attrs={
                    'class':'form-control',
                    'placeholder':'Muñoz'

                }
            ),
            'email':TextInput( 
                attrs={
                    'class':'form-control',
                    'placeholder':'Pedromuñoz@gmail.com'

                }
            )
            
        }


    def __init__(self, *args, **kwargs):
        super(UpdateFormPerfil, self).__init__(*args, **kwargs)
        self.fields['comunidad'].required = True
        self.fields['username'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['edad'].required = True
        self.fields['email'].required = True
        self.fields['confirmar_contraseña'].required = False
        self.fields['nueva_contraseña'].required = False        

    def clean_username(self):
        username = self.cleaned_data['username']
        validate_rut(username)  # Llama a la función de validación personalizada
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        nueva_contraseña = cleaned_data.get("nueva_contraseña")
        confirmar_contraseña = cleaned_data.get("confirmar_contraseña")

        if nueva_contraseña != confirmar_contraseña:
            raise forms.ValidationError("Las contraseñas no coinciden")

        