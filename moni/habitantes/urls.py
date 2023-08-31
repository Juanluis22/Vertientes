from django.urls import path
from habitantes.views import *

app_name='habi'

urlpatterns = [
    
    #selector de comunidades para el admin
    path("lista_vertientes/<int:object_id>/", filtro, name='listvert'),
    path("vertiente/<int:objecto_id>/", revision, name='verti'),
    path("detector/", detector, name='detect'),

    #path("vertiente/<int:object_id>/", filtro, name='vert'),

]