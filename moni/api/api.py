# api/api.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, ProfileSerializer, ComunidadSerializer, VertienteSerializer, KitSerializer, DatosSerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin
from user.models import User, Profile
from nucleo.models import comunidad, vertiente, datos, kit

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        return super().get_permissions()

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

class ComunidadViewSet(viewsets.ModelViewSet):
    queryset = comunidad.objects.all()
    serializer_class = ComunidadSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class VertienteViewSet(viewsets.ModelViewSet):
    queryset = vertiente.objects.all()
    serializer_class = VertienteSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class KitViewSet(viewsets.ModelViewSet):
    queryset = kit.objects.all()
    serializer_class = KitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

class DatosViewSet(viewsets.ModelViewSet):
    queryset = datos.objects.all()
    serializer_class = DatosSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]