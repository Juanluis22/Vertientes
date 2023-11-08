from django.db import models
from django.contrib.auth.models import AbstractUser,Group
from nucleo.models import comunidad
from user.choices import gender_choices, rango_etario

class User(AbstractUser):
    edad = models.CharField(choices=rango_etario, default='No informado', verbose_name='Rango etario')
    comunidad=models.ForeignKey(comunidad, on_delete=models.SET_NULL, null=True, blank=True)
    tipo=models.CharField(max_length=1,null=True,verbose_name='Tipo',default='1')
    is_active = models.BooleanField(default=False)
    token=models.UUIDField(primary_key=False, editable=False, null=True, blank=True )
    gender = models.CharField(choices=gender_choices, default='No informado', verbose_name='Sexo')
    
    #def save(self,*args, **kwargs):
    #    if self.pk is None:
    #        self.set_password(self.password)
    #    super().save(*args,**kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1) 
    token_app_session = models.CharField(max_length = 240,null=True, blank=True, default='')
    first_session = models.CharField(max_length = 240,null=True, blank=True, default='Si')

    class Meta:
        ordering = ['user__username']
