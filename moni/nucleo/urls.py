from django.urls import path
from nucleo.views import *
from crud.views import NuevoUser

app_name='nucleo'

urlpatterns = [

    path("revision/", revision, name='revision'),

    path("login/", InicioSesion.as_view(), name='login'),
    path("logout/", Cerrarsesion.as_view(), name='logout'),
    path("registro/", Registro.as_view(), name='registro'),
    path("recuperar/", Recuperar.as_view(), name='recuperar'),
    
    

]
