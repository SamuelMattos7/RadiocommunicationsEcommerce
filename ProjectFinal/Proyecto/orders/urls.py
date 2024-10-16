from django.urls import path
from . import views
from .views import payment

urlpatterns = [
    path('crear_orders/', views.Crear_orders, name='crear_orders'),
    path('payment/', payment, name='payment'),
    path('payment/execute/', views.execute_payment, name='execute_payment'),
    path('payment/cancel/', views.cancel_payment, name='cancel_payment'),
]