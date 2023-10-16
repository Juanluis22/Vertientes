from django.urls import path
from habitantes.views import *
from habitantes import views

app_name='habi'

urlpatterns = [
    
    #selector de comunidades para el admin
    path("lista_vertientes/<int:object_id>/", filtro, name='listvert'),
    path("vertiente/<int:objecto_id>/<int:objecto_id_2>/", revision, name='verti'),
    path("detector/", detector, name='detect'),
    path('ph/<int:vertiente_id>/', views.grafico_ph, name='grafico_ph'),
    path('caudal/<int:vertiente_id>/', views.grafico_caudal, name='grafico_caudal'),
    path('conductividad/<int:vertiente_id>/', views.grafico_conductividad, name='grafico_conductividad'),
    path('humedad/<int:vertiente_id>/', views.grafico_humedad, name='grafico_humedad'),
    path('temperatura/<int:vertiente_id>/', views.grafico_temperatura, name='grafico_temperatura'),
    path('turbiedad/<int:vertiente_id>/', views.grafico_turbiedad, name='grafico_turbiedad'),
    path('miPerfil/<int:pk>/', ActualizarPerfil.as_view(), name='miPerfil'),
    

    #path("vertiente/<int:object_id>/", filtro, name='vert'),

]