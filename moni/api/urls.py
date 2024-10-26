# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import UserViewSet, ProfileViewSet, ComunidadViewSet, VertienteViewSet, KitViewSet, DatosViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'comunidades', ComunidadViewSet)
router.register(r'vertientes', VertienteViewSet)
router.register(r'kits', KitViewSet)
router.register(r'datos', DatosViewSet)

urlpatterns = [
    path('', include(router.urls)),
]