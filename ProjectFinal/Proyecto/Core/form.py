from django import forms
from .models import Producto, TipoProductos, CodigosProductos
from django.core.exceptions import ValidationError

class SoloNumerosValidator:
    def __call__(self, value):
        if not str(value).isdigit():
            raise ValidationError('Este campo solo puede contener números.')

class ProductCreateForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ('Nombre', 'Cantidad', 'Codigos', 'Imagen', 'Tipo',  'Marca', 'Precio', 'pdf_file')
        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'Cantidad': forms.TextInput(attrs={'class': 'form-control'}),
            'Codigos': forms.Select(attrs={'class': 'form-control'}),
            'Tipo': forms.Select(attrs={'class': 'form-control'}),
            'Marca': forms.TextInput(attrs={'class': 'form-control'}),
            'Precio': forms.TextInput(attrs={'class': 'form-control'}),
            'Imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'pdf_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    Cantidad = forms.IntegerField(validators=[SoloNumerosValidator()])
    Precio = forms.IntegerField(validators=[SoloNumerosValidator()])

    def __init__(self, *args, **kwargs):
        super(ProductCreateForm, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['class'] = 'form-control col-12'

class ProductUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Producto
        fields = ['Nombre', 'Cantidad', 'Codigos', 'Tipo', 'Marca', 'Precio', 'Imagen', 'pdf_file']
        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'Cantidad': forms.TextInput(attrs={'class': 'form-control'}),
            'Codigos': forms.TextInput(attrs={'class': 'form-control'}),
            'Tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'Marca': forms.TextInput(attrs={'class': 'form-control'}),
            'Precio': forms.TextInput(attrs={'class': 'form-control'}),
            'Imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'pdf_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProductUpdateForm, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['class'] = 'form-control col-12'

class TipoProductosForm(forms.ModelForm):

    class Meta:
        model = TipoProductos
        fields = ['TipoProducto']
        widgets = {
            'TipoProducto': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(TipoProductosForm, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['class'] = 'form-control col-12'


class CodigoProductosForm(forms.ModelForm):

    class Meta:
        model = CodigosProductos
        fields = ['ProductoCodigo']
        widgets = {
            'Codigo': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(CodigoProductosForm, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['class'] = 'form-control col-12'