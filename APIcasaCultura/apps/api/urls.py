from django.conf.urls import url, include
from tastypie.api import Api
from django.contrib import admin
from tastypie.api import Api
from resources import *

home_resource = HomeResource()
#capsula_resource = CapsulasResource()
#imagenes_resource = ImagenesResource()
my_api = Api(api_name='cultura')
my_api.register(UserResource())
my_api.register(LoginResource())
my_api.register(ProfileResource())

urlpatterns = [
#     url(r'^', include(api_.urls)),
#     url(r'^', include(capsula_resource.urls)),
#     url(r'^', include(imagenes_resource.urls)),
     url(r'^', include(home_resource.urls)),
     url(r'^', include(my_api.urls))
]
