from orders.models import Orders
from django import forms
from django.core.exceptions import ValidationError

class SoloLetrasValidator:
    def __call__(self, value):
        if not value.isalpha():
            raise ValidationError('Este campo solo puede contener letras.')

class SoloNumerosValidator:
    def __call__(self, value):
        if not value.isdigit():
            raise ValidationError('Este campo solo puede contener números.')

class CreacionOrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ('User', 'User_email', 'Direccion', 'PrecioTotal', 'MetodoPago')

    def __init__(self, *args, **kwargs):
        super(CreacionOrderForm, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['class'] = 'form-control col-6'