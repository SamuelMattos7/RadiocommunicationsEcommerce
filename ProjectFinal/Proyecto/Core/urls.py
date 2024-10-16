from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('Catalogo/', views.Tienda, name='Catalogo'),
    path('add-carrito/<int:ProductID>/', views.Add_Carrito, name='add-carrito'),
    path('VisualizarProducto/<int:ProductID>/', views.ProductoPagina, name='VisualizarProducto'),
    path('quit-carrito/<int:ProductID>/', views.Quit_Carrito, name='quit-carrito'),
    path('AdminProductList', views.VerProduct, name='AdminProductList'),
    path('CrearProduct/', views.CrearProduct, name='CrearProduct'),
    path('ActulizarProduct/<int:id>/', views.UpdateProducto, name='ActulizarProduct'),
    path('EliminarProduct/<int:id>/', views.DeleteProducto, name='EliminarProduct'),    
]