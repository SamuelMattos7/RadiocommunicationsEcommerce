from django.shortcuts import render, get_object_or_404
from django.views import generic
from Core.models import Producto
from django.http import HttpResponseRedirect
from .form import ProductUpdateForm, ProductCreateForm, TipoProductosForm, CodigoProductosForm
from django.urls import reverse 
from django.shortcuts import redirect
from cart.models import Carrito, CartItems
from django.contrib.auth.decorators import login_required
from users.models import Usuario
from django_filters.views import FilterView
from .models import Producto
from .filters import ProductFilter
from django.http import Http404, FileResponse
from django.contrib import messages
import os

# Create your views here.
def Home(request): 
    return render(request, template_name="home.html")

def VerProduct(request):

    Item = Producto.objects.all().values()

    template_name = 'productosTest.html'
    
    contexto = {
        'Object': Item,
    }

    return render(request, template_name, contexto)

def CrearProduct(request):
    
    form = ProductCreateForm()

    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.Creado_por = request.user
            producto.save()
            return HttpResponseRedirect(reverse('AdminProductList'))
        else:
            print(form.errors)
            form = ProductCreateForm()


    return render(request, 'CrearProducto.html', {'form':form})
        
def UpdateProducto(request, id):
    instance = get_object_or_404(Producto, ProductID=id)

    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('AdminProductList'))
    else:
        form = ProductUpdateForm(instance=instance)

    return render(request, 'UpdateProductos.html', {'form': form})

def DeleteProducto(request, id):

    instance = get_object_or_404(Producto, ProductID = id)
    product = {'producto': instance}

    if request.method == 'GET':
        return render(request, 'BorrarProducto.html' ,product)
    
    elif request.method == 'POST':
        instance.delete()
        return redirect('AdminProductList')

def TipoProducto(request):
    
    form = TipoProductosForm()

    if request.method == 'POST':
        form = TipoProductosForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('AdminProductList'))
    else:
        print(form.errors)
        form = TipoProductosForm

    return render(request, 'Cods&Types/TipoProducto.html', {'form': form})   

def CodigoProducto(request):

    form = CodigoProductosForm()

    if request.method == 'POST':
        form = CodigoProductosForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('AdminProductList'))
    else:
        print(form.errors)
        form = CodigoProductosForm

    return render(request, 'Cods&Types/CodigoProducto.html', {'form': form})  

def Tienda(request):
    productos = Producto.objects.all()
    context = {'Productos':productos}
    return render(request, 'Tienda/catalogo.html', context)

def ProductoPagina(request, ProductID):

    articulo = get_object_or_404(Producto, ProductID = ProductID)

    producto = {
        'producto' : articulo,
    }

    return render(request, 'Tienda/Producto.html', producto)

@login_required
def Add_Carrito(request, ProductID):

    cliente = request.user

    producto = Producto.objects.get(pk=ProductID)
    carrito, creado = Carrito.objects.get_or_create(UserCart=cliente, Completado=False)
    cart_item, item_created = CartItems.objects.get_or_create(Cart = carrito, Item=producto)

    if not item_created:
        cart_item.Cantidad += 1
    else:
        cart_item.Cantidad = 1

    cart_item.save()

    messages.success(request, "Producto añadido al carrito")

    return redirect('Catalogo')

def Quit_Carrito(request, ProductID):
    producto = Producto.objects.get(pk=ProductID)
    print(f"ProductID: {ProductID}")
    print(f"producto: {producto}")
    cart = Carrito.objects.get(UserCart=request.user, Completado=False)
    
    try:
        cart_item = CartItems.objects.get(Cart=cart, Item=producto)        
        print(f'el producto eliminado fue: {producto}')
        if cart_item.Cantidad >= 1:
            cart_item.delete()
    except CartItems.DoesNotExist:
        pass
    return redirect('carrito')

class ListaProductosView(FilterView):
    model = Producto
    template_name = 'tienda/lista_products.html'
    filterset_class = ProductFilter
    context_object_name = 'productos'

def download_pdf(request, product_id):
    product = get_object_or_404(Producto, ProductID=product_id)

    if not product.pdf_file:
        raise Http404('No hay un archivo asociado con este producto')
    
    file_path = product.pdf_file.path

    if not os.path.exists(file_path):
        raise Http404('Archivo no encontrado')
    
    response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
    return response