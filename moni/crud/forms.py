from django.forms import *
from django.contrib.auth.forms import UserCreationForm
from nucleo.models import *
from user.models import User,Profile
from django import forms

class ComunidadForm(ModelForm):
    class Meta:
        model= comunidad
        fields='__all__'

class VertienteForm(ModelForm):
    class Meta:
        model= vertiente
        fields=['nombre','desc','ubicación','comunidad']
        



class UserForm(ModelForm):
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
            'gender':'Genero',
            'password':'Contraseña',
        }
        help_texts = {
            'username': '',
            'first_name': '',
            'last_name': '',
            'email': '',
            'edad': '',
            'password': '°Le recomendamos escribir una contraseña sencilla, como pueden ser, los ultimos 4 digitos de su RUT.',
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
    )

    tipo = forms.ChoiceField(choices=ROLES, label='Rol')
    class Meta:
        model= User
        fields=['username','first_name','last_name','email',
                'edad','comunidad','tipo','is_active']
        labels={
            'username':'RUT',
            'first_name':'Nombre',
            'last_name':'Apellido',
            'email':'Correo electronico',
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

    