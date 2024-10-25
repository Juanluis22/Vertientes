# serializers.py
from rest_framework import serializers
from .models import comunidad, vertiente, kit, datos

class ComunidadSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo comunidad.
    """
    class Meta:
        model = comunidad
        fields = [
            'id', 'nombre', 'encargado', 'contacto_encargado', 'vertientes', 
            'ubicación', 'latitud', 'longitud'
        ]
        read_only_fields = ['id']

class VertienteSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo vertiente.
    """
    comunidad = ComunidadSerializer(read_only=True)

    class Meta:
        model = vertiente
        fields = [
            'id', 'nombre', 'desc', 'ubicación', 'latitud', 'longitud', 'comunidad'
        ]
        read_only_fields = ['id']

class KitSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo kit.
    """
    vertiente = VertienteSerializer(read_only=True)

    class Meta:
        model = kit
        fields = [
            'id', 'modelo', 'mac', 'is_active', 'created_at', 'modified_at', 'vertiente'
        ]
        read_only_fields = ['id', 'created_at', 'modified_at']

class DatosSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo datos.
    """
    kit = KitSerializer(read_only=True)
    vertiente = VertienteSerializer(read_only=True)

    class Meta:
        model = datos
        fields = [
            'id', 'caudal', 'pH', 'conductividad', 'turbiedad', 'temperatura', 
            'humedad', 'fecha', 'mac', 'kit', 'vertiente'
        ]
        read_only_fields = ['id', 'fecha']