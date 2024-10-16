from django.urls import path
from . import views

urlpatterns = [
    path('carrito/', views.carrito, name='carrito'),
    path('add-cart-item/<int:ProductID>/', views.add, name='AddCartItem'),
    path('rest-cart-item/<int:ProductID>/', views.rest, name='RestCartItem'),
]