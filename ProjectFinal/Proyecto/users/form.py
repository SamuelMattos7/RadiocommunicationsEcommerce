from typing import Any
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from .models import Usuario, Perfil
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class SoloLetrasValidator:
    def __call__(self, value):
        if not value.isalpha():
            raise ValidationError('Este campo solo puede contener letras.')

class SoloNumerosValidator:
    def __call__(self, value):
        if not value.isdigit():
            raise ValidationError('Este campo solo puede contener números.')

class RegistroUsuario(forms.ModelForm):
    
    username_regex = '^[a-zA-Z0-9_]+$'
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    password_regex = '^(?=.*\d)(?=.*[a-zA-Z]).{8,}$'

    username_validator = RegexValidator(
        regex=username_regex,
        message='El nombre de usuario solo puede contener letras, números y guiones bajos (_).'
    )

    email_validator = RegexValidator(
        regex=email_regex,
        message='Por favor, ingrese una dirección de correo electrónico válida.'
    )

    password_validator = RegexValidator(
        regex=password_regex,
        message='La contraseña debe contener al menos una letra y un número, y tener al menos 8 caracteres.'
    )

    # detalla campos a llenar 
    username = forms.CharField(label='cree su nombre de usuario', min_length=6, max_length=30, help_text='requerido', validators=[username_validator])
    email = forms.EmailField(label='Ingrese su correo electronico', min_length=8, max_length=60, help_text='requerido', error_messages={'error':'debe ingresar un correo electronico'}, validators=[email_validator])
    password = forms.CharField(label='Ingrese su contraseña', widget=forms.PasswordInput, validators=[password_validator])
    password2 = forms.CharField(label='Confirme su contraseña', widget=forms.PasswordInput, validators=[password_validator])

    # Indica el modelo y los campos en el cual se ingresa la informacion
    class Meta:
        model = Usuario
        fields = ['username', 'email']

    # funciones que comprueban que los datos esten ingresados correctamente

    def check_username(self):
        username = self.cleaned_data['username'].lower() # toma el nombre de usurio ingresado en el formulario y lo tranforma todo a lowercase
        existe = Usuario.objects.filter(username=username) # valida que el nombre de usuario ingresado, no exista en la base de datos
        # si el username existe lanza error de validacion y indica el porque 
        if existe.count(): 
            raise forms.ValidationError('Este nombre de usuario ya existe')
        return username
    
    def check_email(self):
        email = self.cleaned_data['email'].lower()
        existe = Usuario.objects.filter(email=email)
        if existe.count(): 
            raise forms.ValidationError('Este nombre de email ya esta registrado')
        return email
    
    def check_password2(self):
        passw = self.cleaned_data
        if passw['password'] != passw['password2']:
            raise forms.ValidationError('Las contraseñas ingresadas no coinciden')
        return passw['password2']
    
    def __init__(self, *args, **kwargs):
        super(RegistroUsuario, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['class'] = 'form-control col-12'

class UsuarioLogin(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'password'}))

    def __init__(self, *args, **kwargs):
        super(UsuarioLogin, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['class'] = 'form-control col-12'

class ResetFormPassword(PasswordResetForm):

    email = forms.EmailField(max_length=60, widget=forms.TextInput(attrs={'class':'form-control col-8 mb-3', 'placeholder':'Email', 'id':'email-form'}))

    def email_clean(self):
        email = self.cleaned_data['email']
        usuario = Usuario.objects.filter(email=email)
        if not usuario:
            raise forms.ValidationError('Desafortunadamente no pudimos encontrar su correo en nuestros registros')
        return email

class ResetFormPasswordConfirm(SetPasswordForm):
    password_regex = '^(?=.*\d)(?=.*[a-zA-Z]).{8,}$'

    password_validator = RegexValidator(
        regex=password_regex,
        message='La contraseña debe contener al menos una letra y un número, y tener al menos 8 caracteres.'
    )

    new_password1 = forms.CharField(validators=[password_validator], widget=forms.PasswordInput(attrs={'class': 'form-control mb-2 col-8', 'placeholder': 'Nueva contraseña'}))
    new_password2 = forms.CharField(validators=[password_validator], widget=forms.PasswordInput(attrs={'class': 'form-control mb-2 col-8', 'placeholder': 'Confirme contraseña'}))

class UserUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Usuario
        fields = ['userType',]

    widgets = {
        'userType': forms.TextInput(attrs={'class': 'form-control'}),
    }

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['class'] = 'form-control col-12'

class PerfilCreacionForm(forms.ModelForm):
    
    class Meta:
        model = Perfil
        fields = ['Nombre', 'Apellido', 'Empresa', 'Telefono', 'Region' , 'Direccion']

    widgets = {
        'Nombre': forms.TextInput(attrs={'class': 'form-control'}),
        'Apellido': forms.TextInput(attrs={'class': 'form-control'}),
        'Empresa': forms.TextInput(attrs={'class': 'form-control'}),
        'Telefono': forms.TextInput(attrs={'class': 'form-control'}),
        'Region': forms.Select(attrs={'class': 'form-control'}),
        'Direccion': forms.TextInput(attrs={'class': 'form-control'}),
    }

    Nombre = forms.CharField(validators=[SoloLetrasValidator()])
    Apellido = forms.CharField(validators=[SoloLetrasValidator()])
    Telefono = forms.CharField(validators=[SoloNumerosValidator()])

    def __init__(self, *args, **kwargs):
        super(PerfilCreacionForm, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['class'] = 'form-control col-8'

class PerfilEditarForm(forms.ModelForm):
    
    class Meta:
        model = Perfil
        fields = ['Nombre', 'Apellido', 'Empresa', 'Telefono', 'Region','Direccion']
        labels = {
            'Nombre': 'Nombre',
            'Apellido': 'Apellidos',
            'Empresa': 'Empresa',
            'Telefono': 'Número de Teléfono',
            'Region': 'Region',
            'Direccion': 'Dirección',
        }

    widgets = {
        'Nombre': forms.TextInput(attrs={'class': 'form-control'}),
        'Apellido': forms.TextInput(attrs={'class': 'form-control'}),
        'Empresa': forms.TextInput(attrs={'class': 'form-control'}),
        'Telefono': forms.TextInput(attrs={'class': 'form-control'}),
        'Region': forms.Select(attrs={'class': 'form-control'}),
        'Direccion': forms.TextInput(attrs={'class': 'form-control'}),
    }

    Nombre = forms.CharField(validators=[SoloLetrasValidator()])
    Apellido = forms.CharField(validators=[SoloLetrasValidator()])
    Telefono = forms.CharField(validators=[SoloNumerosValidator()])

    def __init__(self, *args, **kwargs):
        super(PerfilEditarForm, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['class'] = 'form-control col-8'
