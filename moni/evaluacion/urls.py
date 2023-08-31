from django.urls import path
from evaluacion.views import *

app_name='eva'

urlpatterns = [
    
    #selector de comunidades para el admin
    path("selector/", Comunidades.as_view(), name='comuni'),

]