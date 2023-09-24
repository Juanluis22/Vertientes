from django.urls import path
from nucleo.views import *
from crud.views import NuevoUser
from nucleo import views

app_name='nucleo'

urlpatterns = [

    path("revision/", revision, name='revision'),

    path("login/", InicioSesion.as_view(), name='login'),
    path("logout/", Cerrarsesion.as_view(), name='logout'),
    path("registro/", Registro.as_view(), name='registro'),
    path("recuperar/", Recuperar.as_view(), name='recuperar'),
    path("recuperar/contraseña/", ResetPasswordView.as_view(), name='recuperar'),
    path("cambio/contraseña/<str:token>", ChangePasswordView.as_view(), name='cambio'),
    path('users_massive_upload/',views.users_massive_upload,name="users_massive_upload"),
    path('users_massive_upload_save/',views.users_massive_upload_save,name="users_massive_upload_save"),
    path('users_import_file/',views.users_import_file,name="users_import_file"),
    path("anidado/", Select_anidado.as_view(), name='select'),


]
