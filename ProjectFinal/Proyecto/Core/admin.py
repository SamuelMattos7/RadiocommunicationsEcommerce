from django.contrib import admin
from .models import Producto, CodigosProductos, TipoProductos
# Register your models here.

admin.site.register(Producto)
admin.site.register(CodigosProductos)
admin.site.register(TipoProductos)