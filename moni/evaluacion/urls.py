from django.urls import path
from evaluacion.views import *

app_name='eva'

urlpatterns = [
    
    #selector de comunidades para el admin
    path('admin/comunidades/', ComunidadesAdmin.as_view(), name='comuni'),
    path('autoridad/comunidades/', ComunidadesAutoridad.as_view(), name='comuni_autoridad'),
]