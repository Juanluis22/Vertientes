from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from nucleo.models import comunidad
from user.choices import gender_choices, rango_etario

class User(AbstractUser):
    """
    Modelo personalizado de usuario que extiende el modelo AbstractUser de Django.
    """
    edad = models.CharField(
        choices=rango_etario, 
        default='No informado', 
        verbose_name='Rango etario'
    )
    comunidad = models.ForeignKey(
        comunidad, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    tipo = models.CharField(
        max_length=20, 
        null=True, 
        verbose_name='Tipo', 
        default='Usuario'
    )
    is_active = models.BooleanField(default=False)
    token = models.UUIDField(
        primary_key=False, 
        editable=False, 
        null=True, 
        blank=True
    )
    gender = models.CharField(
        choices=gender_choices, 
        default='No informado', 
        verbose_name='Sexo'
    )
    
    # Método save personalizado (comentado)
    # def save(self, *args, **kwargs):
    #     if self.pk is None:
    #         self.set_password(self.password)
    #     super().save(*args, **kwargs)

class Profile(models.Model):
    """
    Modelo de perfil que está relacionado uno a uno con el modelo User.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1)
    token_app_session = models.CharField(
        max_length=240, 
        null=True, 
        blank=True, 
        default=''
    )
    first_session = models.CharField(
        max_length=240, 
        null=True, 
        blank=True, 
        default='Si'
    )
    
    objects = models.Manager()  # Add this line to ensure 'objects' manager exists

    class Meta:
        """
        Meta class for specifying model options.

        Attributes:
            ordering (list): Specifies the default ordering for the model's objects, 
                             in this case, by the 'username' field of the related 'user' model.
        """
        ordering = ['user__username']