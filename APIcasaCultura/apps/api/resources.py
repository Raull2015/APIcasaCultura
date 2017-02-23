from django.contrib.auth.models import User
from django.db import IntegrityError

from tastypie.resources import ModelResource, Resource
from tastypie.serializers import Serializer
from tastypie.authorization import DjangoAuthorization, ReadOnlyAuthorization, Authorization
from tastypie.authentication import BasicAuthentication
from tastypie.exceptions import BadRequest
from tastypie import fields
from datetime import date

from models import *

class ActividadResource(ModelResource):
    imagenes = fields.ToManyField('apps.api.resources.ImagenesResource', 'imagenes_set' ,  related_name='actividad' )
    class Meta:
        queryset = Actividad.public.all().order_by('-fechaRealizacion')
        limit = 6
        fields = ['nombre', 'lugar', 'fechaRealizacion', 'hora', 'descripcion', 'fechaPublicacion', 'puntuacion', 'coordenadas']
        authorization = Authorization()
        serializer = Serializer(formats=['json'])
        resource_name = 'act'

class ArtistasResource(ModelResource):
    class Meta:
        queryset = Perfil.public.all()
        limit = 10
        fields =['nombreArtista','nombreReal','imagen','sexo','fechaNacimiento','telefono','']
        list_allowed_methods = ['get']
        authorization = Authorization()
        serializer = Serializer(formats=['json'])
        resource_name = 'art'

class ImagenesResource(ModelResource):
    actividad = fields.ToOneField(ActividadResource, 'actividad')
    class Meta:
        queryset = Imagenes.objects.all()
        fields = ['imagen']
        serializer = Serializer(formats=['json'])
        authorization = Authorization()
        resource_name = 'img'

class CapsulasResource(ModelResource):
    class Meta:
        queryset = Capsulas.objects.all()
        limit = 10
        fields = ['texto', 'imagen']
        serializer = Serializer(formats=['json'])
        authorization = Authorization()
        resource_name = 'cap'

class CategoriaResource(ModelResource):
    class Meta:
        #object_class = Categoria
        queryset = Categoria.objects.all()
        resource_name = 'cat'
        allowed_methods = ['post', 'get']
        authorization = Authorization()
        serializer = Serializer(formats=['json'])

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

class UserResource(ModelResource):
	class Meta:
		object_class = User
		queryset = User.objects.all()
		resource_name = "user"
		fields = ['username']
		allowed_methods = ['post', 'get']
		include_resource_uri = False
		authorization = Authorization()
		serializer = Serializer(formats=['json'])
    	def obj_create(self, bundle, request=None, **kwargs):
        	try:
				bundle = super(CreateUserResource, self).obj_create(bundle)
				bundle.obj.set_password(bundle.data.get('password'))
				bundle.obj.save()
        	except IntegrityError:
				raise BadRequest('El usuario ya existe')

    		return bundle

class LoginResource(ModelResource):
    class Meta:
		allowed_methods = ['get']
		resource_name = 'login'
		include_resource_uri = False
		object_class = User
		excludes = ['password']
		authentication = BasicAuthentication()
		authorization = Authorization()
		serializer = Serializer(formats=['json'])

    def obj_get_list(self, bundle, **kwargs):
        return [bundle.request.user]

class ProfileResource(ModelResource):
    user = fields.OneToOneField(UserResource, 'user')
    #actividad = fields.ManyToManyField(ActivdadResource, 'actividad')
    #categoria = fields.ManyToManyField(CategoriaResource,'categoria')
    class Meta:
        queryset = Perfil.objects.all()
        allowed_methods = ['post', 'get']
        limit = 10
        authorization = Authorization()
        serializer = Serializer(formats=['json'])
        resource_name = 'per'
