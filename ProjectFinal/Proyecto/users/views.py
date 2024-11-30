from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from .hash import Hash_Activacion_Cuenta
from users.form import RegistroUsuario, UserUpdateForm, PerfilCreacionForm, PerfilEditarForm
from .models import Usuario, Perfil
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse
from orders.models import Orders
import pandas as pd
import matplotlib
import matplotlib.dates as mdates
import csv
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.utils.timezone import now
import os
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.core.files.base import ContentFile
from io import BytesIO

# Create your views here.

@login_required
def MenuUser(request):
    return render(request, 'usuario/MenuUser.html')

def Users(request):
    return render(request, 'users.html')

def Registro(request):

    if request.user.is_authenticated:
        return redirect('perfil')
     
    if request.method == 'POST':

        form = RegistroUsuario(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email'] 
            user.set_password(form.cleaned_data['password'])
            user.is_active = False 
            user.save()

            current_site = get_current_site(request)
            asunto = 'Activacion de Cuenta ReidioSolutions'
            mensaje = render_to_string('Activacion_Cuentas.html', 
                {
                    'user':user,
                    'domain':current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': Hash_Activacion_Cuenta.make_token(user),
                }
            )
            user.email_user(subject=asunto, message=mensaje)
            return redirect('home')
        else:
            form = RegistroUsuario()
            return render(request, 'registro.html', {'form':form})
        
    form = RegistroUsuario()
    return render(request, 'registro.html', {'form': form})

def Activacion_Cuenta(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Usuario.objects.get(pk=uid)
    except():
        pass
    if user is not None and Hash_Activacion_Cuenta.check_token(user, token):
        user.is_active =True
        user.save()
        login(request, user)
        return redirect('CrearPerfil')
    else:
        return render(request, 'Activacion_Cuenta_Invalida.html')

def Admins(request):
    return render(request, 'administrador/AdminPanel.html')

def ListaUsers(request):

    users = Usuario.objects.all().values()

    template_name = 'administrador/Usuarios.html'
    
    contexto = {
        'Object': users,
    }

    return render(request, template_name, contexto)

def DeleteUsers(request, id):

    instance = get_object_or_404(Usuario, UserID = id)
    users = {'users': instance}

    if request.method == 'GET':
        return render(request, 'administrador/BorrarUser.html' ,users)
    
    elif request.method == 'POST':
        instance.delete()
        return redirect('AdminUsersList')

def UpdateUser(request, id):
    
    instance = get_object_or_404(Usuario, UserID = id)

    if request.method == 'POST':
        
        form = UserUpdateForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('AdminUserList'))
    else:
        form = UserUpdateForm(instance=instance)

    return render(request, 'administrador/UpdateUser.html', {'form': form})

def ver_orders(request):
    orders = Orders.objects.prefetch_related('Items__Item').all()

    contexto = {
        'Object': orders,
    }

    return render(request, 'administrador/ordersAdmin.html', contexto)

def CrearPerfil(request):

    if request.method == 'POST':
        form = PerfilCreacionForm(request.POST)

        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.User = request.user
            perfil.save()
            return redirect('perfil')
        else:
            print(form.errors)
            form = PerfilCreacionForm()

    form = PerfilCreacionForm()
    return render(request, 'perfil/PerfilForm.html', {'form':form})

def verPerfil(request):
    perfil = Perfil.objects.get(User=request.user)
    contexto = {'perfil': perfil}
    return render(request, 'perfil/perfil.html', contexto)

def editarPerfil(request):

    perfil = Perfil.objects.get(User=request.user)

    if request.method == 'POST':

        form = PerfilEditarForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil')
        else:
            print(form.errors)
            form = PerfilEditarForm()
    else:
        form = PerfilEditarForm(instance=perfil)

    return render(request, 'perfil/EditarPerfil.html', {'form':form})

def aboutus(request):
    return render(request, 'informacion/aboutus.html')

def contact(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')

        Mensaje_Completo  = f"Nombre: {nombre}\nCorreo: {email}\n\nMensaje:\n{mensaje}"

        send_mail(
            subject=asunto,
            message=Mensaje_Completo,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['reidiosolutions@gmail.com'],  
            fail_silently=False,
        )

        return HttpResponse("Mensaje enviado exitosamente.")

    return render (request, 'informacion/contact.html')

def download_orders(request):
    if request.method == 'POST':
        orders = Orders.objects.all()
        order_data = []
        order_items_data = []

        for order in orders:
            cart_items = order.Items.all()
            items_detail = []

            for item in cart_items:
                order_items_data.append({
                    'OrderID': order.OrderID,
                    'Nombre_Producto': item.Item.Nombre,
                    'Tipo_Producto': item.Item.Tipo.TipoProducto,
                    'Precio': item.Item.Precio,
                    'Cantidad': item.Cantidad,
                    'FechaCompra': order.FechaCompra.strftime('%Y-%m-%d %H:%M:%S'),
                    'region_User': order.User_region
                })

                items_detail.append(f"{item.Item.Nombre} (Tipo: {item.Item.Tipo.TipoProducto}, Precio: {item.Item.Precio}, Cantidad: {item.Cantidad})")

            items_string = "; ".join(items_detail)

            order_data.append({
                'OrderID': order.OrderID,
                'User': order.User.username,  
                'User_email': order.User_email,
                'User_region': order.User_region,
                'Direccion': order.Direccion,
                'MetodoPago': order.MetodoPago,
                'Items': items_string,  
                'PrecioTotal': order.PrecioTotal,
                'FechaCompra': order.FechaCompra.strftime('%Y-%m-%d %H:%M:%S')
            })

        df_orders = pd.DataFrame(order_data)
        
        df_order_items = pd.DataFrame(order_items_data)

        from io import BytesIO
        import zipfile

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            
            orders_csv = df_orders.to_csv(sep=';', index=False)
            zip_file.writestr('orders.csv', orders_csv)
            
            order_items_csv = df_order_items.to_csv(sep=';', index=False)
            zip_file.writestr('order_items.csv', order_items_csv)

        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=orders_export.zip'
        
        return response

    return render(request, 'administrador/download_orders.html')

def Power_bi_panel(request):
    return render(request, 'administrador/PowerBiPanel.html')