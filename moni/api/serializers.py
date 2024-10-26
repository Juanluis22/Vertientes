# serializers.py
from rest_framework import serializers
from user.models import User, Profile
from nucleo.models import comunidad, vertiente, kit, datos

ROLES = (
    ('Usuario', 'Usuario'),
    ('Autoridad', 'Autoridad'),
    ('Administrador', 'Administrador')
)

class UserSerializer(serializers.ModelSerializer):
    tipo = serializers.ChoiceField(choices=ROLES)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'is_active', 'edad', 
            'comunidad', 'tipo', 'gender'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password', 'autocomplete': 'new-password'}}
        }

    def create(self, validated_data):
        tipo = validated_data.pop('tipo')
        user = User.objects.create_user(**validated_data)
        if tipo == 'Usuario':
            group_id = 2
        elif tipo == 'Autoridad':
            group_id = 3
        elif tipo == 'Administrador':
            group_id = 1
        Profile.objects.create(user=user, group_id=group_id)
        profile = Profile.objects.get(user=user)
        print(f"User created while registering: {user}, Profile created with group id: {group_id}, Profile details: {profile}")
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'group', 'first_session']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        profile = Profile.objects.create(user=user, **validated_data)
        return profile
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
        
    

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