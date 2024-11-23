from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.mail import send_mail
from django.conf import settings
# Create your models here.

class ManejoDeCuentas(BaseUserManager):
    
    #Maneja la creacion del superusuario
    def create_superuser(self, email, username, password, **other_fields):

        #Marca como default los siguientes campos
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        #Valida los campos default del superuauario 
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser el campo de staff debe ser designado como verdadero(True)')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser el campo de superuser debe ser designado como verdadero(True)')
        
        #
        return self.create_user(email, username, password, **other_fields)
    
    def create_user(self, email, username, password, **other_fields):

        if not email: 
            raise ValueError('Debe entregar su correo electronico')
        
        email = self.normalize_email(email) # Normaliza el correo el electronico, chequea si se ha formateado correctamente
        user = self.model(email=email, username=username, **other_fields) # se crea el objeto user, listo para ser guardado a la DB
        user.set_password(password) # determinamos la contraseña del ususario
        user.save() # se guarda la informacion
        # retornamos el usuario
        return user
            

class Usuario(AbstractBaseUser, PermissionsMixin):
    
    ROL = (
        ('ADMINISTRADOR', 'Admin'),
        ('VENDEDOR', 'Seller'),
        ('CLIENTE', 'Cliente'),
    )

    UserID = models.AutoField(verbose_name='UserID', primary_key=True)
    email = models.EmailField(verbose_name='Email', max_length=60, unique=True)
    username = models.CharField(verbose_name='username', max_length=30, unique=True)
    userType = models.CharField(verbose_name='Tipo de usuario', max_length=25, choices=ROL, default='CLIENTE')
    
    #Estado del usuario
    is_active= models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    #Fechas de creacion o modificacion del usuario
    creado= models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    objects = ManejoDeCuentas()

    USERNAME_FIELD = 'email' # Toma el rol de nombre de usuario 
    REQUIRED_FIELDS = ["username"] # Campos requeridos

    #La meta data
    class Meta:
        verbose_name = "Cuentas"
        verbose_name_plural = "Cuentas"

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'settings.EMAIL_HOST_USER',
            [self.email],
            fail_silently = False
        )

    def __str__(self):
        return self.username

class Perfil(models.Model):

    Regiones = (
        (1, "Arica y Parinacota"),
        (2, "Tarapacá"),
        (3, "Antofagasta"),
        (4, "Atacama"),
        (5, "Coquimbo"),
        (6, "Valparaíso"),
        (7, "Región Metropolitana de Santiago"),
        (8, "Libertador General Bernardo O'Higgins"),
        (9, "Maule"),
        (10, "Ñuble"),
        (11, "Biobío"),
        (12, "La Araucanía"),
        (13, "Los Ríos"),
        (14, "Los Lagos"),
        (15, "Aysén del General Carlos Ibáñez del Campo"),
        (16, "Magallanes y de la Antártica Chilena")
    )

    PerfilID = models.AutoField(primary_key=True, verbose_name='PerfilID')
    User = models.OneToOneField(settings.AUTH_USER_MODEL, to_field='UserID', on_delete=models.CASCADE)
    Nombre = models.CharField(verbose_name="Nombre cliente", max_length=30)
    Apellido = models.CharField(verbose_name="Apellido cliente", max_length=30)
    afiliacion = models.CharField(verbose_name='afiliacion', max_length=60, unique=False, null=True)
    Telefono = models.CharField(verbose_name="Telefono cliente", max_length=30)
    Region = models.CharField(verbose_name='Region', max_length=25, choices=Regiones, default=7, null=True)
    Direccion = models.CharField(verbose_name="Direccion cliente", max_length=30)