from django.urls import path  # Importa la función path para definir rutas de URL
from habitantes.views import *  # Importa todas las vistas desde habitantes.views
from habitantes import views  # Importa el módulo views desde habitantes

app_name = 'habi'  # Define el espacio de nombres para las URLs de la aplicación

urlpatterns = [
    # Selector de comunidades para el admin
    path("lista_vertientes/<int:object_id>/", filtro, name='listvert'),  # Ruta para filtrar vertientes por comunidad
    path("vertientes_admin/<int:objecto_id>/", revision_admin, name='verti_admin'),  # Ruta para la revisión de vertientes por el admin
    path("vertiente/<int:objecto_id>/<int:objecto_id_2>/", revision, name='verti'),  # Ruta para la revisión de una vertiente específica
    path("detector/", detector, name='detect'),  # Ruta para el detector
    path("vertientes/<int:objecto_id>/", revision_autoridad, name='verti_autoridad'),  # Ruta para la revisión de vertientes por la autoridad

    # Gráficos
    path('grafico/<str:tipo_grafico>/<int:vertiente_id>/', views.grafico_generico, name='grafico_generico'),  # Ruta para generar gráficos genéricos
    path('miPerfil/<int:pk>/', ActualizarPerfil.as_view(), name='miPerfil'),  # Ruta para actualizar el perfil del usuario

    # URL para actualización automática de los datos de vertientes
    path('sse_datos/<int:objecto_id>/', views.sse_datos, name='sse_datos'),  # Ruta para la actualización automática de datos de vertientes
    path('sse_grafico/<int:vertiente_id>/<str:tipo_grafico>/<str:date_range>/', views.sse_grafico, name='sse_grafico'),  # Ruta para la actualización automática de gráficos
]