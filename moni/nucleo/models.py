from django.db import models
from datetime import datetime

# Create your models here.
class comunidad(models.Model):
    nombre=models.CharField(max_length=150,verbose_name='Nombre')
    vertientes=models.PositiveIntegerField(default=0)
    ubicación=models.CharField(max_length=200,verbose_name='Ubicación')

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name='Comunidad'
        verbose_name_plural='Comunidades'
        db_table='comunidad'
        ordering=['id']




class vertiente(models.Model):
    nombre=models.CharField(max_length=150,verbose_name='Nombre')
    desc=models.CharField(max_length=250,verbose_name='Descripcion')
    ubicación=models.CharField(max_length=200,verbose_name='Ubicación')
    comunidad=models.ForeignKey(comunidad, on_delete=models.SET_NULL, null=True)

    caudal=models.IntegerField(default=0)
    pH=models.IntegerField(default=0)
    conductividad=models.IntegerField(default=0)
    turbiedad=models.IntegerField(default=0)
    temperatura=models.IntegerField(default=0)
    humedad=models.IntegerField(default=0)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name='Vertiente'
        verbose_name_plural='Vertientes'
        db_table='vertiente'
        ordering=['id']




class kit(models.Model):
    modelo=models.IntegerField(default=0)
    ubicación=models.CharField(max_length=200,verbose_name='Ubicación')

    def __str__(self):
        return self.modelo
    
    class Meta:
        verbose_name='Kit'
        verbose_name_plural='Kits'
        db_table='Kit'
        ordering=['id']





class datos(models.Model):
    caudal=models.IntegerField(default=0)
    pH=models.IntegerField(default=0)
    conductividad=models.IntegerField(default=0)
    turbiedad=models.IntegerField(default=0)
    temperatura=models.IntegerField(default=0)
    humedad=models.IntegerField(default=0)

    vertiente=models.ForeignKey(vertiente, on_delete=models.SET_NULL, null=True)
    kit=models.ForeignKey(kit, on_delete=models.SET_NULL, null=True)
    fecha=models.DateTimeField(auto_now=True)

    
    
    class Meta:
        verbose_name='Dato'
        verbose_name_plural='Datos'
        db_table='datos'
        ordering=['id']




