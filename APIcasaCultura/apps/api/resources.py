from tastypie.resources import ModelResource, Resource
from tastypie.serializers import Serializer
from tastypie.authorization import DjangoAuthorization, ReadOnlyAuthorization
from tastypie import fields
from datetime import date
from models import *

class ActividadResource(ModelResource):
    imagenes = fields.ToManyField('apps.api.resources.ImagenesResource', 'imagenes_set' ,  related_name='actividad' )
    class Meta:
        queryset = Actividad.public.all().order_by('-fechaRealizacion')
        limit = 6
        fields = ['nombre', 'lugar', 'fechaRealizacion', 'hora', 'descripcion', 'fechaPublicacion', 'puntuacion', 'coordenadas']
        serializer = Serializer(formats=['json'])
        resource_name = 'act'

class ArtistasResource(ModelResource):
    class Meta:
        queryset = Perfil.public.all()
        limit = 10
        fields =[]
        serializer = Serializer(formats=['json'])
        resource_name = 'art'

class ImagenesResource(ModelResource):
    actividad = fields.ToOneField(ActividadResource, 'actividad')
    class Meta:
        queryset = Imagenes.objects.all()
        fields = ['imagen']
        serializer = Serializer(formats=['json'])
        resource_name = 'img'

class CapsulasResource(ModelResource):
    class Meta:
        queryset = Capsulas.objects.all()
        limit = 10
        fields = ['texto', 'imagen']
        serializer = Serializer(formats=['json'])
        resource_name = 'cap'

class HomeResource(ActividadResource):
    #imagenes = fields.ToManyField(ImagenPortadaResource, 'imagenes_set' ,  related_name='actividad', full=True )
    class Meta:
        queryset = Actividad.public.all().order_by('-fechaRealizacion')
        limit = 6
        fields = ['id', 'nombre', 'lugar', 'fechaRealizacion', 'hora']
        serializer = Serializer(formats=['json'])
        list_allowed_methods = ['get']
        authorization = ReadOnlyAuthorization()
        resource_name = 'home'

    def dehydrate(self, bundle):
        bundle.data['imagen'] = None
        try:
            img = Imagenes.objects.filter(actividad=int(bundle.data['id']))[0]
            bundle.data['imagen'] = '/media/' + str(img.imagen)
        except IndexError:
            pass
        return bundle

    def alter_list_data_to_serialize(self, request, data):
        del data['meta']
        data['capsula'] = {}
        try:
            cap = Capsulas.objects.all().filter(fechaPublicacion__range=('2016-01-01', date.today())).order_by('-fechaPublicacion')[0]
            data['capsula']['texto'] = cap.texto
            data['capsula']['imagen'] = cap.imagen
        except IndexError:
            pass
        return data
