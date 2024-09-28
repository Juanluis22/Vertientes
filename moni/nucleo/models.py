from django.db import models  # Importa el módulo models de Django para definir modelos
from datetime import datetime  # Importa la clase datetime para trabajar con fechas y horas

# Define el modelo comunidad
class comunidad(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombre')  # Nombre de la comunidad
    encargado = models.CharField(max_length=100, verbose_name='Encargado', null=False, blank=False)  # Nombre del encargado
    contacto_encargado = models.CharField(max_length=100, verbose_name='Contacto del encargado', null=False, blank=False)  # Contacto del encargado
    vertientes = models.PositiveIntegerField(default=0, null=True, blank=True)  # Número de vertientes
    ubicación = models.CharField(max_length=200, verbose_name='Ubicación', null=True, blank=True)  # Ubicación de la comunidad
    latitud = models.FloatField(null=True, blank=True)  # Latitud de la comunidad
    longitud = models.FloatField(null=True, blank=True)  # Longitud de la comunidad

    def __str__(self):
        return self.nombre  # Representación en cadena del modelo

    class Meta:
        verbose_name = 'Comunidad'  # Nombre singular del modelo
        verbose_name_plural = 'Comunidades'  # Nombre plural del modelo
        db_table = 'comunidad'  # Nombre de la tabla en la base de datos
        ordering = ['id']  # Ordenamiento por defecto

# Define el modelo vertiente
class vertiente(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombre')  # Nombre de la vertiente
    desc = models.CharField(max_length=250, verbose_name='Descripcion', null=True, blank=True)  # Descripción de la vertiente
    ubicación = models.CharField(max_length=200, verbose_name='Ubicación', null=True, blank=True)  # Ubicación de la vertiente
    latitud = models.FloatField(null=True, blank=True)  # Latitud de la vertiente
    longitud = models.FloatField(null=True, blank=True)  # Longitud de la vertiente

    comunidad = models.ForeignKey(comunidad, on_delete=models.SET_NULL, null=True)  # Relación con el modelo comunidad

    def __str__(self):
        return self.nombre  # Representación en cadena del modelo

    class Meta:
        verbose_name = 'Vertiente'  # Nombre singular del modelo
        verbose_name_plural = 'Vertientes'  # Nombre plural del modelo
        db_table = 'vertiente'  # Nombre de la tabla en la base de datos
        ordering = ['id']  # Ordenamiento por defecto

# Define el modelo kit
class kit(models.Model):
    modelo = models.IntegerField(default=0)  # Modelo del kit
    mac = models.CharField(max_length=25, verbose_name='Direccion MAC', null=True, blank=True)  # Dirección MAC del kit
    is_active = models.BooleanField(default=False)  # Estado de activación del kit
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación del kit
    modified_at = models.DateTimeField(auto_now=True)  # Fecha de última modificación del kit

    vertiente = models.ForeignKey(vertiente, on_delete=models.SET_NULL, null=True)  # Relación con el modelo vertiente

    def __str__(self):
        return str(self.modelo)  # Representación en cadena del modelo

    class Meta:
        verbose_name = 'Kit'  # Nombre singular del modelo
        verbose_name_plural = 'Kits'  # Nombre plural del modelo
        db_table = 'Kit'  # Nombre de la tabla en la base de datos
        ordering = ['id']  # Ordenamiento por defecto

# Define el modelo datos
class datos(models.Model):
    caudal = models.FloatField(default=0)  # Caudal de la vertiente
    pH = models.FloatField(default=0)  # pH de la vertiente
    conductividad = models.FloatField(default=0)  # Conductividad de la vertiente
    turbiedad = models.FloatField(default=0)  # Turbiedad de la vertiente
    temperatura = models.FloatField(default=0)  # Temperatura de la vertiente
    humedad = models.FloatField(default=0)  # Humedad de la vertiente
    fecha = models.DateTimeField(auto_now=True)  # Fecha de registro de los datos

    mac = models.CharField(max_length=25, verbose_name='Direccion MAC', null=True, blank=True)  # Dirección MAC del kit
    kit = models.ForeignKey(kit, on_delete=models.SET_NULL, null=True)  # Relación con el modelo kit
    vertiente = models.ForeignKey(vertiente, on_delete=models.SET_NULL, null=True)  # Relación con el modelo vertiente

    class Meta:
        verbose_name = 'Dato'  # Nombre singular del modelo
        verbose_name_plural = 'Datos'  # Nombre plural del modelo
        db_table = 'datos'  # Nombre de la tabla en la base de datos
        ordering = ['id']  # Ordenamiento por defecto