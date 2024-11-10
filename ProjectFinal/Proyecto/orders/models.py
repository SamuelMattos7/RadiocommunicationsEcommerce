from django.db import models
from cart.models import CartItems
from users.models import Perfil
from django.conf import settings

# Create your models here.
class Orders(models.Model):
    OrderID = models.AutoField(verbose_name='OrderID', primary_key=True)
    User =models.ForeignKey(settings.AUTH_USER_MODEL, to_field='UserID', on_delete=models.CASCADE)
    User_email = models.EmailField(verbose_name='User_email', max_length=60, null=True)
    Direccion = models.CharField(verbose_name='Direccion', max_length=60)
    MetodoPago = models.CharField(verbose_name='MetodoPago', default='PayPal', max_length=30)
    Items = models.ManyToManyField(CartItems)
    PrecioTotal = models.IntegerField(verbose_name="Precio Compra")
    FechaCompra = models.DateTimeField(verbose_name="Fecha de compra", auto_now_add=True)