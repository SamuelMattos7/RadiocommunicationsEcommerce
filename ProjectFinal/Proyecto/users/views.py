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
# Create your views here.

@login_required
def MenuUser(request):
    return render(request, 'usuario/MenuUser.html')

def Users(request):
    return render(request, 'users.html')

def Registro(request):

    if request.user.is_authenticated:
        return redirect('users')
     
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
        return redirect('users')
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
            return redirect('users')
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

    return render(request, 'perfil/EditarPerfil.html', {'form':form}),

def aboutus(request):
    return render(request, 'informacion/aboutus.html')

def contact(request):
    return render (request, 'informacion/contact.html')
    
            
