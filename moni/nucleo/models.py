from django.db import models
from datetime import datetime

# Create your models here.
class comunidad(models.Model):
    nombre=models.CharField(max_length=150,verbose_name='Nombre')
    encargado=models.CharField(max_length=100,verbose_name='Encargado',null=False, blank=False)
    contacto_encargado=models.CharField(max_length=100,verbose_name='Contacto del encargado',null=False, blank=False)
    vertientes=models.PositiveIntegerField(default=0,null=True, blank=True)
    ubicación=models.CharField(max_length=200,verbose_name='Ubicación',null=True, blank=True)
    latitud=models.FloatField(null=True, blank=True)
    longitud=models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name='Comunidad'
        verbose_name_plural='Comunidades'
        db_table='comunidad'
        ordering=['id']




class vertiente(models.Model):
    nombre=models.CharField(max_length=150,verbose_name='Nombre')
    desc=models.CharField(max_length=250,verbose_name='Descripcion',null=True, blank=True)
    ubicación=models.CharField(max_length=200,verbose_name='Ubicación',null=True, blank=True)
    latitud=models.FloatField(null=True, blank=True)
    longitud=models.FloatField(null=True, blank=True)

    comunidad=models.ForeignKey(comunidad, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name='Vertiente'
        verbose_name_plural='Vertientes'
        db_table='vertiente'
        ordering=['id']




class kit(models.Model):
    modelo=models.IntegerField(default=0)
    mac=models.CharField(max_length=25,verbose_name='Direccion MAC',null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    vertiente=models.ForeignKey(vertiente, on_delete=models.SET_NULL, null=True)

    # Se borra el atributo ubicaion, ya que se encuentra en la entidad vertiente
    # ubicacion=models.CharField(max_length=200,verbose_name='Ubicación',null=True, blank=True)

    def __str__(self):
        return str(self.modelo)
    
    class Meta:
        verbose_name='Kit'
        verbose_name_plural='Kits'
        db_table='Kit'
        ordering=['id']





class datos(models.Model):
    caudal = models.FloatField(default=0)
    pH = models.FloatField(default=0)
    conductividad = models.FloatField(default=0)
    turbiedad = models.FloatField(default=0)
    temperatura = models.FloatField(default=0)
    humedad = models.FloatField(default=0)
    fecha=models.DateTimeField(auto_now=True)
    
    mac=models.CharField(max_length=25,verbose_name='Direccion MAC',null=True, blank=True)
    kit=models.ForeignKey(kit, on_delete=models.SET_NULL, null=True)
    vertiente=models.ForeignKey(vertiente, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name='Dato'
        verbose_name_plural='Datos'
        db_table='datos'
        ordering=['id']


