from tastypie.resources import ModelResource
from tastypie import fields
from datetime import date
from models import *

class ActividadResource(ModelResource):
    imagenes = fields.ToManyField('apps.api.resources.ImagenesResource', 'imagenes_set' ,  related_name='actividad', full=True )
    class Meta:
        queryset = Actividad.public.all().order_by('-fechaRealizacion')
        limit = 6
        fields = ['nombre', 'lugar', 'fechaRealizacion', 'hora']
        resource_name = 'act'

class ImagenesResource(ModelResource):
    #actividad = fields.ToOneField(ActividadResource, 'actividad').use_in
    class Meta:
        queryset = Imagenes.objects.all()
        fields = ['imagen']
        resource_name = 'img'


class CapsulasResource(ModelResource):
    class Meta:
        queryset = Capsulas.objects.all().filter(fechaPublicacion__range=('2016-01-01', date.today())).order_by('-fechaPublicacion')
        limit = 1
        fields = ['texto', 'imagen']
        resource_name = 'cap'
