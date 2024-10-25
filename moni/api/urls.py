from django.urls import path
from api.views import UserList, UserDetail, ProfileList, ProfileDetail, ComunidadList, ComunidadDetail, VertienteList, VertienteDetail, KitList, KitDetail

urlpatterns = [
    # URLs para User
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),

    # URLs para Profile
    path('profiles/', ProfileList.as_view(), name='profile-list'),
    path('profiles/<int:pk>/', ProfileDetail.as_view(), name='profile-detail'),

    # URLs para Comunidad
    path('comunidades/', ComunidadList.as_view(), name='comunidad-list'),
    path('comunidades/<int:pk>/', ComunidadDetail.as_view(), name='comunidad-detail'),

    # URLs para Vertiente
    path('vertientes/', VertienteList.as_view(), name='vertiente-list'),
    path('vertientes/<int:pk>/', VertienteDetail.as_view(), name='vertiente-detail'),

    # URLs para Kit
    path('kits/', KitList.as_view(), name='kit-list'),
    path('kits/<int:pk>/', KitDetail.as_view(), name='kit-detail'),
]