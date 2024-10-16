from django.shortcuts import render, redirect
from . models import *
# Create your views here.
def carrito(request):
    if request.user.is_authenticated:
        cliente = request.user
        carrito, creado = Carrito.objects.get_or_create(UserCart=cliente, Completado=False)
        items = carrito.Carrito.all()
        total = carrito.PrecioTotal()
        cantidad = carrito.CantidadTotal()

    else:
        items = []
        total = 0
        cantidad = 0
    
    context = {'items':items, 'total':total, 'cantidad':cantidad}
    return render(request, 'carrito.html', context)

def add(request, ProductID):

    cliente = request.user

    producto = Producto.objects.get(pk=ProductID)    
    carrito = Carrito.objects.get(UserCart=cliente, Completado=False)
    cart_item, item_created = CartItems.objects.get_or_create(Cart=carrito.CartID, Item=producto)

    cart_item.Cantidad += 1
    cart_item.save()
    return redirect('carrito')
    
def rest(request, ProductID):
    cliente = request.user

    producto = Producto.objects.get(pk=ProductID)    
    carrito = Carrito.objects.get(UserCart=cliente)
    cart_item, item_created = CartItems.objects.get_or_create(Cart=carrito.CartID, Item=producto)

    if cart_item.Cantidad > 1:
        cart_item.Cantidad -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('carrito')