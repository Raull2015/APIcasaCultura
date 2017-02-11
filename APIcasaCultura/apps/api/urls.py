from django.conf.urls import url, include
from django.contrib import admin
from resources import *

#actividad_resource = ActividadResource()
#capsula_resource = CapsulasResource()
#imagenes_resource = ImagenesResource()
home_resource = HomeResource()

urlpatterns = [
#     url(r'^', include(actividad_resource.urls)),
#     url(r'^', include(capsula_resource.urls)),
#     url(r'^', include(imagenes_resource.urls)),
     url(r'^', include(home_resource.urls)),
]
