from django.urls import path
from . import views
from .views import ListaProductosView

urlpatterns = [
    path('', views.Home, name='home'),
    path('Catalogo/', views.Tienda, name='Catalogo'),
    path('SearchProductos/', ListaProductosView.as_view(), name='SearchProductos'),
    path('add-carrito/<int:ProductID>/', views.Add_Carrito, name='add-carrito'),
    path('VisualizarProducto/<int:ProductID>/', views.ProductoPagina, name='VisualizarProducto'),
    path('quit-carrito/<int:ProductID>/', views.Quit_Carrito, name='quit-carrito'),
    path('AdminProductList', views.VerProduct, name='AdminProductList'),
    path('CrearProduct/', views.CrearProduct, name='CrearProduct'),
    path('ActulizarProduct/<int:id>/', views.UpdateProducto, name='ActulizarProduct'),
    path('EliminarProduct/<int:id>/', views.DeleteProducto, name='EliminarProduct'), 
    path('TipoProducto/', views.TipoProducto, name='TipoProducto'),
    path('CodigoProducto/', views.CodigoProducto, name='CodigoProducto'),
    path('download_pdf/<int:product_id>/', views.download_pdf, name='download_pdf'),
]