from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PerfilManager(models.Manager):
    def get_queryset(self):
        qs = super(PerfilManager, self).get_queryset()
        return qs.filter(autorizado=1)

class ActividadManager(models.Manager):
    def get_queryset(self):
        qs = super(ActividadManager, self).get_queryset()
        return qs.filter(autorizado=1)

class CapsulaManager(models.Manager):
    def get_queryset(self):
        qs = super(CapsulaManager, self).get_queryset()
        return qs.filter(fechaPublicacion=date.today())


class Actividad(models.Model):
    nombre = models.CharField(max_length=200)
    lugar = models.CharField(max_length=200)
    fechaRealizacion = models.DateField('Fecha a realizar')
    hora = models.TimeField('Hora de Realizacion')
    descripcion = models.TextField(max_length=800)
    #imagen = models.ImageField(upload_to='imgActividad/', default='imgActividad/default.jpg')
    fechaPublicacion = models.DateField('Fecha de publicacion')
    puntuacion = models.IntegerField(default=0)
    #visitas = models.IntegerField(default=0)
    autorizado = models.SmallIntegerField(default=0)
    #categoria = models.ManyToManyField(Categoria)
    #perfil = models.ManyToManyField(Perfil,db_index=True)
    coordenadas = models.CharField(max_length=100, null=True, blank=True)  #add
    #perfil = models.ManyToManyField(Perfil)
    objects = models.Manager()
    public = ActividadManager()

    class Meta:
        verbose_name = 'actividad'
        verbose_name_plural = 'actividades'
        ordering = ['-fechaRealizacion']

    def __unicode__(self):
        return self.nombre

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    categoria = models.CharField(max_length=100)
    actividad = models.ManyToManyField(Actividad)   #add
    objects = models.Manager()

    def __str__(self):
        return self.categoria

    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'


class Perfil(models.Model):
    nombreArtista = models.CharField(max_length=100)
    nombreReal = models.CharField(max_length=65)
    imagen = models.ImageField(upload_to='imgPerfil/', default='imgPerfil/default.jpg')
    sexo = models.SmallIntegerField(default=0)
    fechaNacimiento = models.DateField('Fecha de nacimiento')
    telefono = models.CharField(max_length=16)
    email= models.EmailField('Correo')
    biografia= models.TextField(blank=True, null=True)  #add
    #descripcion = models.CharField(max_length=200)
    fechaRegistro = models.DateField('Fecha de registro', auto_now_add=True)
    #visitas = models.IntegerField(default=0)
    autorizado = models.SmallIntegerField(default=0)
    categoria = models.ManyToManyField(Categoria)
    actividad = models.ManyToManyField(Actividad)
    #rol = models.ForeignKey(Rol)
    user =  models.OneToOneField(User, on_delete=models.CASCADE)
    objects = models.Manager()
    public = PerfilManager()

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfiles'
        ordering = ['-fechaRegistro']

    def __unicode__(self):
        return self.nombreArtista

    def __str__(self):
        return self.nombreArtista


#Numero de visitas que recibe el Perfil
class VisitasPerfil(models.Model):
    cantidad = models.IntegerField(default=0)
    fecha = models.DateField()

    class Meta:
        verbose_name = 'visitaperfil'
        verbose_name_plural = 'visitasperfiles'
        ordering = ['-fecha']

''''
class Usuarios(models.Model)

    user = models.CharField(max_length=50)
    contrasenia = models.CharField(max_length=25)
    ultimaConexion = models.DateField()

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        ordering = ['-ultimaConexion']
'''
class Rol(models.Model):
    nombreRol = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=45)
    perfil = models.ForeignKey(Perfil, blank=True, null=True)  #add
    #perfil = PerfilManager()    #add
    objects = models.Manager()

    def __str__(self):
        return self.nombreRol

    def is_admin(self):
        if self.nombreRol == 'Administrador':
            return True

    def is_artista(self):
        if self.nombreRol == 'Artista':
            return True

    class Meta:
        verbose_name = 'rol'
        verbose_name_plural = 'roles'

#   Una Actividad puede tener muchas imagenes
class Imagenes(models.Model):
    imagen = models.ImageField(upload_to='imgActividad/', default='imgActividad/default.jpg')
    actividad = models.ForeignKey(Actividad, null=False, blank=False, on_delete=models.CASCADE)
    objects = models.Manager()
    class Meta:
        verbose_name = 'imagen'
        verbose_name_plural = 'imagenes'


#   Numero de Visitas que recibe una Actividad
class VisitasActividad(models.Model):
    cantidad = models.IntegerField(default=0)
    fecha = models.DateField()
    actividad = models.ForeignKey(Actividad, null=False, blank=False)

    class Meta():
        verbose_name = 'visitactividad'
        verbose_name_plural = 'visitasactividades'


class Comentarios(models.Model):
    contenido = models.TextField(max_length=200)
    fechaComentario = models.DateField('Fecha del comentario')
    actividad = models.ForeignKey(Actividad)
    perfil = models.ForeignKey(Perfil, blank=True, null=True)  #add
    def __str__(self):
        return self.contenido

    class Meta:
        verbose_name = 'comentario'
        verbose_name_plural = 'comentarios'


class Capsulas(models.Model):
    fechaPublicacion = models.DateField('Fecha de publicacion')
    texto = models.TextField(max_length=225)
    #autorizado = models.SmallIntegerField(default=1)
    #usuario = models.ForeignKey(User)
    perfil = models.ForeignKey(Perfil, blank=True, null=True)  #add
    imagen = models.ImageField(upload_to='imgCapsula/', default='imgCapsula/default.jpg')
    objects = models.Manager()
    public = CapsulaManager()


    def __str__(self):
        return self.texto

    class Meta:
        verbose_name = 'capsula'
        verbose_name_plural = 'capsulas'
