from django.shortcuts import render
from cart.models import Carrito
from orders.form import CreacionOrderForm
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse 
import paypalrestsdk
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings


paypalrestsdk.configure({
    'mode':'sandbox',
    'client_id':'AVG3zJOOJxQijsUEVVGqVdG_Cx4emRL6AnjTStbRaxBvSk9etUa5NxaoBTCmuFYIW2lx8lfttAB7xaLo',
    'client_secret':'EI4yGMMvehpl0wyh2F0N25GiqL7TxvXkAR2wF71nypWtzRCk1iFVEe0lTkqLoRmX6EHmwPHA_Hjg3zjp'
})

# Create your views here.
def Crear_orders(request):

    if request.user.is_authenticated:
        cliente = request.user
        carrito = Carrito.objects.get(UserCart=cliente, Completado=False)
        items = carrito.Carrito.all()
        total = carrito.PrecioTotal()
        cantidad = carrito.CantidadTotal()
    else:
        items = []
        total = 0
        cantidad = 0
    
    context = {'items':items, 'total':total, 'cantidad':cantidad}
    
    return render(request, 'orders.html', context)

@login_required
def payment(request):

    cliente = request.user
    carrito = get_object_or_404(Carrito, UserCart=cliente, Completado=False)
    items = carrito.Carrito.all()

    transactions = [{
        'item_list': {
            'items': [{
                'name': A.Item.Nombre,
                'sku': str(A.Item.Codigos),
                'price': str(A.Item.Precio),
                'currency': 'USD',  
                'quantity': A.Cantidad,
            } for A in items]
        },
        'amount': {
            'total': str(carrito.PrecioTotal()),  
            'currency': 'USD', 
        },
        'description': 'Payment for items in the cart'
    }]


    return_url = reverse('execute_payment') 
    cancel_url = reverse('cancel_payment')

    payment = paypalrestsdk.Payment({
        'intent':'sale',
        'payer':{
            'payment_method':'paypal'
        },
        'redirect_urls': {
            'return_url': request.build_absolute_uri(return_url),
            'cancel_url': request.build_absolute_uri(cancel_url),
        },
        'transactions':transactions
    })

    if payment.create():
        return JsonResponse({"payment_url": payment.links[1].href})
    else:
        return JsonResponse({"error": payment.error})

def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    token = request.GET.get('token')

    print(f"Payment ID: {payment_id}, Payer ID: {payer_id}, Token: {token}")

    if payer_id is None:
        return render(request, 'pagos/error.html', {'error': 'Payment canceled or Payer ID missing'})

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({'payer_id': payer_id}):
        return confirmar_order(request)
    else:
        return render(request, 'pagos/error.html', {'error': 'Payment execution failed'})
    
def cancel_payment(request):
    return render(request, 'pagos/cancel_payment.html')

def confirmar_order(request):
    carrito = Carrito.objects.get(UserCart=request.user, Completado=False)
    items = carrito.Carrito.all()
    print(items)

    form = CreacionOrderForm({
        'User':request.user, 
        'User_email':request.user.email,
        'User_region':request.user.perfil.Region,
        'Direccion':request.user.perfil.Direccion,
        'MetodoPago':'Paypal',
        'PrecioTotal': carrito.PrecioTotal(),
    })

    if form.is_valid():
        with transaction.atomic():
            order = form.save(commit=False)
            order.save()
            carrito.Completado = True
            carrito.save()
            for cart_item in items:
                order.Items.add(cart_item)
            print('Orden Creada')

            subject = 'Creacion de pedido'
            message = f'Querido {request.user.username}, \n\nTu pedido se a realizado correctamente. \n\nDetalles de pedido:'
            for item in items:
                message+= f'{item.Item.Nombre} - Cantidad: {item.Cantidad} - Precio: {item.Item.Precio}\n'
            message+= f'n\Precio Total: ${carrito.PrecioTotal()}\n\nGracias por su compra!'
            recipient = request.user.email

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient],
                fail_silently=False,
            )
    else:
        print(form.errors)

    return render(request, 'pagos/execute_payment.html', {'error': 'Pago y creacion de su orden realizados exitosamente'})