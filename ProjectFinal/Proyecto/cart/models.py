from django.db import models
from django.conf import settings 
from django.core.validators import MinValueValidator
from Core.models import Producto
    
class Carrito(models.Model):
    CartID= models.AutoField(primary_key=True, verbose_name='CartID')
    Fecha_Creado = models.DateTimeField(auto_now_add=True)
    UserCart= models.ForeignKey( 
        settings.AUTH_USER_MODEL, 
        to_field='UserID', 
        related_name='CarritoDeUser',
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True 
    )
    Completado = models.BooleanField(default=False, null=True, blank=False)

    def PrecioTotal(self):
        cart_Items = self.Carrito.all()  
        TotalPrice = sum(item.Total for item in cart_Items)
        return TotalPrice
    
    def CantidadTotal(self):
        cart_Items = self.Carrito.all()  
        TotalPrice = sum(item.Cantidad for item in cart_Items)
        return TotalPrice

class CartItems(models.Model):
    CartItemsID = models.AutoField(primary_key=True, verbose_name='XID')
    Cart = models.ForeignKey(
        Carrito,
        to_field='CartID',
        related_name='Carrito',
        on_delete=models.CASCADE
    )
    Item = models.ForeignKey(
        Producto, 
        to_field='ProductID',
        related_name='Items', 
        on_delete= models.CASCADE,
    )
    Cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    fechaAgregado = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.Item.Nombre
    
    @property
    def Total(self):
        total = self.Item.Precio * self.Cantidad
        return total
    

    

