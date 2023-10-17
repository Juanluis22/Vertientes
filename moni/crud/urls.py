from django.urls import path
from crud.views import *

app_name='crud'

urlpatterns = [
    
    #Selector
    path("selector/", Select.as_view(), name='select'),


    #index
    path("indice/", Indice.as_view(), name='index'),


    #indice general
    path("indiceComunidad/", IndiceCom.as_view(), name='indcom'),
    path("indiceVertiente/", IndiceVert.as_view(), name='indvert'),


    #Listas
    path("lista_comunidad/", ListaComunidad.as_view(), name='listcom'),
    path("lista_vertiente/", ListaVertiente.as_view(), name='listvert'),
    path("lista_usuarios/", ListaUsuarios.as_view(), name='listauser'),
    path("lista_peticiones/", ListaPeticion.as_view(), name='listpet'),
    

    #Creación
    path("nueva_comunidad/", NuevaComunidad.as_view(), name='newcom'),
    path("nuevo_user/", NuevoUser.as_view(), name='newuser'),
    path("nueva_vertiente/", NuevaVertiente.as_view(), name='newvert'),


    #Actualizacion
    path("actualizacion_usuarios/<int:pk>/", ActualizarUsuario.as_view(), name='updateuser'),
    path("actualizacion_vertientes/<int:pk>/", ActualizarVertiente.as_view(), name='updatevert'),
    path("actualizacion_comunidades/<int:pk>/", ActualizarComunidad.as_view(), name='updatecom'),

    #Eliminación
    path("eliminar_comunidad/<int:pk>/", EliminarComunidad.as_view(), name='deletecom'),
    path("eliminar_usuario/<int:pk>/", EliminarUsuario.as_view(), name='deleteUser'),
    path("eliminar_vertiente/<int:pk>/", EliminarVertiente.as_view(), name='deletevert'),




    #Activación
    path("activación/<int:pk>/", activar_estado, name='activaruser'),

    #Desactivación
    path("desactivar/<int:pk>/", desactivar_estado, name='deactuser'),

    
    





    
    

    #Prueba
    path("prueba/", Prueba.as_view(), name='prueba'),


]