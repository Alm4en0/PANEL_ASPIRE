from django.urls import path
from . import views
from django.urls import path, re_path
from .views import  get_curso_by_nombre, save_payment, loginMovil, iniciar_pago_paypal, confirmar_pago_paypal
from rest_framework.authtoken import views as drf_views
from django.urls import re_path



urlpatterns = [
    path('categorias/', views.CategoriaCursoListCreate.as_view(), name='categoria-list-create'),
    path('categorias/<int:pk>/', views.CategoriaCursoRetrieveUpdateDestroy.as_view(), name='categoria-detail'),

    path('subcategorias/', views.SubCategoriaCursoListCreate.as_view(), name='subcategoria-list-create'),
    path('subcategorias/<int:pk>/', views.SubCategoriaCursoRetrieveUpdateDestroy.as_view(), name='subcategoria-detail'),

    path('cursos/', views.CursoListCreate.as_view(), name='curso-list-create'),
    path('cursos/<int:pk>/', views.CursoRetrieveUpdateDestroy.as_view(), name='curso-detail'),

    path('planes/', views.PlanListCreate.as_view(), name='plan-list-create'),
    path('planes/<int:pk>/', views.PlanRetrieveUpdateDestroy.as_view(), name='plan-detail'),

    path('ventas/', views.VentaListCreate.as_view(), name='venta-list-create'),
    path('ventas/<int:pk>/', views.VentaRetrieveUpdateDestroy.as_view(), name='venta-detail'),

    path('planes-curso/', views.PlanCursoListCreate.as_view(), name='plan-curso-list-create'),
    path('planes-curso/<int:pk>/', views.PlanCursoRetrieveUpdateDestroy.as_view(), name='plan-curso-detail'),

    path('inscripciones-curso/', views.InscripcionCursoListCreate.as_view(), name='inscripcion-curso-list-create'),
    path('inscripciones-curso/<int:pk>/', views.InscripcionCursoRetrieveUpdateDestroy.as_view(), name='inscripcion-curso-detail'),

    path('ventas-curso/', views.VentaCursoListCreate.as_view(), name='venta-curso-list-create'),
    path('ventas-curso/<int:pk>/', views.VentaCursoRetrieveUpdateDestroy.as_view(), name='venta-curso-detail'),

    path('modulos-curso/', views.ModuloCursoListCreate.as_view(), name='modulo-curso-list-create'),
    path('modulos-curso/<int:pk>/', views.ModuloCursoRetrieveUpdateDestroy.as_view(), name='modulo-curso-detail'),

    path('recursos-curso/', views.RecursoCursoListCreate.as_view(), name='recurso-curso-list-create'),
    path('recursos-curso/<int:pk>/', views.RecursoCursoRetrieveUpdateDestroy.as_view(), name='recurso-curso-detail'),

    path('ventas-pago/', views.VentaPagoListCreate.as_view(), name='venta-pago-list-create'),
    path('ventas-pago/<int:pk>/', views.VentaPagoRetrieveUpdateDestroy.as_view(), name='venta-pago-detail'),

    path('registros-landing/', views.RegistroLandingListCreate.as_view(), name='registro-landing-list-create'),
    path('registros-landing/<int:pk>/', views.RegistroLandingRetrieveUpdateDestroy.as_view(), name='registro-landing-detail'),


    path('usuarios/', views.CustomUserListCreate.as_view()),  # Ruta para listar y crear usuarios
    path('usuarios/<int:pk>/', views.CustomUserRetrieveUpdateDestroy.as_view()),  # Ruta para obtener, actualizar y eliminar usuarios

    path('login/', views.login, name='login'),
    path('loginMovil/', views.loginMovil, name='loginMovil'),
    path('register/', views.register, name='register'),
    path('api-token-auth/', drf_views.obtain_auth_token),  # Ruta para obtener el token de autenticación


    
    re_path(r'^cursos/(?P<nombre>[\w-]+)/$', get_curso_by_nombre),
    path('save-payment/', views.save_payment, name='save_payment'),
    path('iniciar-pago/', views.iniciar_pago_paypal, name='iniciar_pago_paypal'),
    path('confirmar-pago/', views.confirmar_pago_paypal, name='confirmar_pago_paypal'),


]