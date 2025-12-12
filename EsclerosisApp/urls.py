from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.inicio_esclerosis, name='inicio'),
    path('api/fundaciones/', views.api_fundaciones, name='api_fundaciones'),


    # -------------------- Sección info sobre EM --------------------
    path('sobre/comprender/', views.comprender_em, name='que_es_em'),
    path('sobre/evaluacion/', views.evaluacion, name='deteccion'),
    path('sobre/apoyo/', views.apoyo_y_tratamiento, name='tratamientos'),
    path('sobre/programas/', views.programas_publicos, name='programas_publicos'),
    path('sobre/material/', views.material_educativo, name='recursos'),

    # -------------------- Sección testimonios --------------------
    path('testimonios/', views.testimonios, name='testimonios'),
    path('testimonios/nuevo/', views.crear_testimonio, name='crear_testimonio'),

    path('testimonios/editar/<int:id>/', views.verificar_rut_editar, name='verificar_rut_editar'),
    path('testimonios/editar/form/<int:id>/', views.editar_testimonio, name='editar_testimonio'),

    path('testimonios/eliminar/dueno/<int:id>/', views.eliminar_testimonio_dueno, name='eliminar_testimonio_dueno'),
    path('testimonios/eliminar/admin/<int:id>/', views.eliminar_testimonio_admin, name='eliminar_testimonio_admin'),
    path('fundaciones/eliminar/aprobada/<int:id>/', views.eliminar_fundacion_aprobada, name='eliminar_fundacion_aprobada'),

    # -------------------- Fundaciones --------------------
    path('fundaciones/', views.fundaciones, name='fundaciones'),
    path('fundaciones/aprobar/<int:id>/', views.aprobar_fundacion, name='aprobar_fundacion'),
    path('fundaciones/rechazar/<int:id>/', views.rechazar_fundacion, name='rechazar_fundacion'),

    # -------------------- FUNDACIONES CRUD --------------------
    path('fundaciones/crear/', views.crear_fundacion, name='crear_fundacion'),
    path('fundaciones/aprobar/<int:id>/', views.aprobar_fundacion, name='aprobar_fundacion'),
    path('fundaciones/eliminar/<int:id>/', views.eliminar_fundacion, name='eliminar_fundacion'),

    # -------------------- Contacto --------------------
    path('contacto/', views.contacto, name='contacto'),
    path('contacto/eliminar/<int:id>/', views.eliminar_mensaje_contacto, name='eliminar_mensaje_contacto'),

    # -------------------- Registro / Login --------------------
    path('registro-admin/', views.registro_admin, name='registro_admin'),
    path('login/', auth_views.LoginView.as_view(template_name='formularios/login.html'), name='login'),
    path('salir/', views.custom_logout_view, name='custom_logout'),
    path('registro/', views.registro_usuario, name='registro_usuario'),
]
