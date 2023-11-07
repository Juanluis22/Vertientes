from django.urls import path
from habitantes.views import *
from habitantes import views

app_name='habi'

urlpatterns = [
    #selector de comunidades para el admin
    path("lista_vertientes/<int:object_id>/", filtro, name='listvert'),
    path("vertientes_admin/<int:objecto_id>/", revision_admin, name='verti_admin'),
    path("vertiente/<int:objecto_id>/<int:objecto_id_2>/", revision, name='verti'),
    path("detector/", detector, name='detect'),

    path("vertientes/<int:objecto_id>/", revision_autoridad, name='verti_autoridad'),
    




    

    # Gráficos
    path('grafico/<str:tipo_grafico>/<int:vertiente_id>/', views.grafico_generico, name='grafico_generico'),
    
    path('miPerfil/<int:pk>/', ActualizarPerfil.as_view(), name='miPerfil'),
    
    # URL para actualizacion automatica de los datos de vertientes
    path('sse_datos/<int:objecto_id>/', views.sse_datos, name='sse_datos'),

    path('sse_grafico/<int:vertiente_id>/<str:tipo_grafico>/<str:date_range>/', views.sse_grafico, name='sse_grafico'),


]

