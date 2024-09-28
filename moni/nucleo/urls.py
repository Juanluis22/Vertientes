from django.urls import path  # Importa la función path para definir rutas de URL
from nucleo.views import *  # Importa todas las vistas desde nucleo.views
from crud.views import NuevoUser  # Importa la vista NuevoUser desde crud.views
from nucleo import views  # Importa el módulo views desde nucleo

app_name = 'nucleo'  # Define el espacio de nombres para las URLs de la aplicación

urlpatterns = [
    # Ruta para la vista de revisión
    path("revision/", revision, name='revision'),
    # Ruta para la vista de inicio
    path("", Inicio.as_view(), name='inicio'),
    # Ruta para la vista de inicio de sesión
    path("login/", InicioSesion.as_view(), name='login'),
    # Ruta para la vista de cierre de sesión
    path("logout/", Cerrarsesion.as_view(), name='logout'),
    # Ruta para la vista de registro de usuarios
    path("registro/", Registro.as_view(), name='registro'),
    # Ruta para la vista de recuperación de contraseña
    path("recuperar/contraseña/", ResetPasswordView.as_view(), name='recuperar'),
    # Ruta para la vista de cambio de contraseña con un token
    path("cambio/contraseña/<str:token>", ChangePasswordView.as_view(), name='cambio'),
    # Rutas para la carga masiva de usuarios
    path('users_massive_upload/', views.users_massive_upload, name="users_massive_upload"),
    path('users_massive_upload_save/', views.users_massive_upload_save, name="users_massive_upload_save"),
    path('users_import_file/', views.users_import_file, name="users_import_file"),
    # Rutas para la carga masiva de vertientes
    path('vertiente_massive_upload/', views.vertiente_massive_upload, name="vertiente_massive_upload"),
    path('vertiente_massive_upload_save/', views.vertiente_massive_upload_save, name="vertiente_massive_upload_save"),
    path('vertiente_import_file/', views.vertiente_import_file, name="vertiente_import_file"),
    # Rutas para la carga masiva de kits
    path('kit_massive_upload/', views.kit_massive_upload, name="kit_massive_upload"),
    path('kit_massive_upload_save/', views.kit_massive_upload_save, name="kit_massive_upload_save"),
    path('kit_import_file/', views.kit_import_file, name="kit_import_file"),
    # Rutas para la carga masiva de comunidades
    path('comunity_massive_upload/', views.comunity_massive_upload, name="comunity_massive_upload"),
    path('comunity_massive_upload_save/', views.comunity_massive_upload_save, name="comunity_massive_upload_save"),
    path('comunity_import_file/', views.comunity_import_file, name="comunity_import_file"),
    # Ruta para la vista de selección anidada
    path("anidado/", Select_anidado.as_view(), name='select'),
    # Ruta para la vista del mapa con un ID de objeto
    path("mapa/<int:objecto_id>/", mapa, name='mapa'),
]