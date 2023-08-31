from django.db import models
from django.contrib.auth.models import AbstractUser
from nucleo.models import comunidad

class User(AbstractUser):
    edad=models.IntegerField(blank=True,default=0)
    comunidad=models.ForeignKey(comunidad, on_delete=models.SET_NULL, null=True)
    tipo=models.CharField(max_length=1,null=True,verbose_name='Tipo',default='a')
    is_active = models.BooleanField(default=False)

    #def save(self,*args, **kwargs):
    #    if self.pk is None:
    #        self.set_password(self.password)
    #    super().save(*args,**kwargs)