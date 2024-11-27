import django_filters
from django.db import models
from .models import Producto, TipoProductos, CodigosProductos
from django import forms

class ProductFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='filter_by_all', 
        label='Buscar',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar...'})
    )
    precio_min = django_filters.NumberFilter(
        field_name='Precio', 
        lookup_expr='gte', 
        label='Precio es mayor que o igual a:',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min'})
    )
    precio_max = django_filters.NumberFilter(
        field_name='Precio', 
        lookup_expr='lte', 
        label='Precio es menor que o igual a:',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max'})
    )
    tipo = django_filters.ModelChoiceFilter(
        queryset=TipoProductos.objects.all(),
        field_name='Tipo',
        label='Tipo:',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    codigo = django_filters.ModelChoiceFilter(
        queryset=CodigosProductos.objects.all(),
        field_name='Codigos',
        label='Codigos:',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta: 
        model = Producto
        fields = ['precio_min', 'precio_max', 'tipo', 'codigo']

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(
            models.Q(Nombre__icontains=value) | models.Q(Marca__icontains=value)
        )