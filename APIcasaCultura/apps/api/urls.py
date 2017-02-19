from django.conf.urls import url, include
from django.contrib import admin
from tastypie.api import Api
from resources import *

#actividad_resource = ActividadResource()
#capsula_resource = CapsulasResource()
#imagenes_resource = ImagenesResource()
home_resource = HomeResource()
my_api = Api(api_name='cultura')
my_api.register(UserResource())
my_api.register(LoginResource())
my_api.register(ProfileResource())

urlpatterns = [
#     url(r'^', include(actividad_resource.urls)),
#     url(r'^', include(capsula_resource.urls)),
#     url(r'^', include(imagenes_resource.urls)),
     url(r'^', include(home_resource.urls)),
     url(r'^', include(my_api.urls))
]
