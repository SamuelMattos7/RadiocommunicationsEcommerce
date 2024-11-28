from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from users.form import UsuarioLogin, ResetFormPassword, ResetFormPasswordConfirm
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Users, name='users'),
    path('CrearPerfil/', views.CrearPerfil, name='CrearPerfil'),
    path('Perfil/', views.verPerfil, name='perfil'),
    path('EditarPerfil/', views.editarPerfil, name='EditarPerfil'),
    path('registro/', views.Registro, name='registro'),
    path('activar/<slug:uidb64>/<slug:token>/', views.Activacion_Cuenta, name='activar'),
    path('login/', auth_views.LoginView.as_view(template_name='usuario/login.html', form_class=UsuarioLogin), name='login'),
    path('ResetPassword/', auth_views.PasswordResetView.as_view(
        template_name='usuario/passwordReset.html', 
        success_url='Mail_Reset_Password', 
        email_template_name='usuario/passwordResetMail.html',
        form_class=ResetFormPassword), 
        name='PasswordReset'),
    path('password_reset_confirmacion/<slug:uidb64>/<slug:token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='usuario/PasswordResetConfirmacion.html',
        success_url='Password_Reset_Completado/',
        form_class=ResetFormPasswordConfirm),
        name='password_reset_confirmacion'),
    path('ResetPassword/Mail_Reset_Password/', TemplateView.as_view(template_name='usuario/reset_situacion.html'), name='password_reset_exito'),
    path('password_reset_confirmacion/MQ/Password_Reset_Completado/', TemplateView.as_view(template_name='usuario/reset_situacion.html'), name='password_reset_finalizado'),
    path('logout/', auth_views.LogoutView.as_view(http_method_names=['get', 'post'], next_page='/users/login/'), name='logout'),
    path('AdminPanel/', views.Admins, name='AdminPanel'),
    path('AdminUserList/', views.ListaUsers, name='AdminUserList'),
    path('AdminOrderList/', views.ver_orders, name='AdminOrderList'),
    path('EliminarUser/<int:id>/', views.DeleteUsers, name='EliminarUser'),
    path('ActualizarUser/<int:id>/', views.UpdateUser,name='ActualizarUser'),
    path('download_orders/', views.download_orders, name='download_orders'),
    path('PowerBiPanel/', views.Power_bi_panel, name='PowerBiPanel'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('contact/', views.contact, name='contact')
]