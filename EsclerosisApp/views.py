from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group

from .forms import (
    RegistroAdminForm,
    TestimonioVerificadoForm,
    VerificarRutForm,
    CustomUserCreationForm,
    ContactoForm,
    FundacionPropuestaForm,  
)

from .models import (
    TestimonioVerificado,
    Profile,
    MensajeContacto,
    FundacionPropuesta,      
)


# -------------------- Registro de administrador --------------------
def registro_admin(request):
    if request.method == 'POST':
        form = RegistroAdminForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Administrador creado correctamente.")
            return redirect('inicio')
        messages.error(request, "Revisa los errores del formulario.")
    else:
        form = RegistroAdminForm()
    return render(request, 'formularios/registro_admin.html', {'form': form})


# -------------------- Página de inicio --------------------
def inicio_esclerosis(request):

    fundaciones_preview = FundacionPropuesta.objects.filter(aprobada=True)

    return render(request, 'inicio_esclerosis.html', {
        'fundaciones_preview': fundaciones_preview
    })
def comprender_em(request):
    return render(request, 'sobre_em/comprender_em.html')

def evaluacion(request):
    return render(request, 'sobre_em/evaluacion.html')

def apoyo_y_tratamiento(request):
    return render(request, 'sobre_em/apoyo_y_tratamiento.html')

def programas_publicos(request):
    return render(request, 'sobre_em/programas_publicos.html')

def material_educativo(request):
    return render(request, 'sobre_em/material_educativo.html')


# -------------------- Testimonios --------------------
def testimonios(request):
    busqueda = request.GET.get('q', '')
    orden = request.GET.get('orden', '')

    testimonios = TestimonioVerificado.objects.all()

    if busqueda:
        testimonios = testimonios.filter(titulo__icontains=busqueda)

    if orden == 'az':
        testimonios = testimonios.order_by('titulo')
    elif orden == 'za':
        testimonios = testimonios.order_by('-titulo')
    else:
        testimonios = testimonios.order_by('-fecha_envio')

    return render(request, 'testimonios.html', {
        'testimonios': testimonios,
        'busqueda': busqueda,
        'orden': orden
    })


# -------------------- Crear testimonio --------------------
def crear_testimonio(request):
    if request.method == 'POST':
        form = TestimonioVerificadoForm(request.POST)
        if form.is_valid():
            testimonio = form.save(commit=False)

            if request.user.is_authenticated:
                try:
                    usuario_rut = request.user.profile.rut
                except Profile.DoesNotExist:
                    messages.error(request, "Tu perfil no tiene RUT asociado.")
                    return render(request, 'formularios/testimonios_form.html', {'form': form})

                if usuario_rut != testimonio.rut:
                    messages.error(request, "El RUT ingresado no coincide con el de tu cuenta.")
                    return render(request, 'formularios/testimonios_form.html', {'form': form})

                testimonio.user = request.user

            testimonio.save()
            messages.success(request, "Tu testimonio se publicó correctamente.")
            return redirect('testimonios')
        messages.error(request, "Revisa los errores del formulario.")
    else:
        initial_data = {}
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            try:
                initial_data['rut'] = request.user.profile.rut
            except Profile.DoesNotExist:
                pass

        form = TestimonioVerificadoForm(initial=initial_data)

    return render(request, 'formularios/testimonios_form.html', {'form': form})


# -------------------- Verificar RUT para editar --------------------
def verificar_rut_editar(request, id):
    testimonio = get_object_or_404(TestimonioVerificado, id=id)

    if request.user.is_authenticated:
        try:
            if request.user.profile.rut == testimonio.rut:
                return redirect('editar_testimonio', id=testimonio.id)
            messages.error(request, "No puedes editar un testimonio que no es tuyo.")
            return redirect('testimonios')
        except Profile.DoesNotExist:
            pass

    if request.method == 'POST':
        form = VerificarRutForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['rut'] == testimonio.rut:
                return redirect('editar_testimonio', id=testimonio.id)
            messages.error(request, "RUT incorrecto.")
    else:
        form = VerificarRutForm()

    return render(request, 'formularios/verificar_rut.html', {
        'form': form,
        'accion': 'editar'
    })


# -------------------- Editar testimonio --------------------
def editar_testimonio(request, id):
    testimonio = get_object_or_404(TestimonioVerificado, id=id)

    if request.method == 'POST':
        form = TestimonioVerificadoForm(request.POST, instance=testimonio)
        if form.is_valid():
            form.save()
            messages.success(request, "El testimonio fue actualizado.")
            return redirect('testimonios')
        messages.error(request, "Revisa los errores del formulario.")
    else:
        form = TestimonioVerificadoForm(instance=testimonio)

    return render(request, 'formularios/testimonios_form.html', {
        'form': form,
        'editar': True
    })


# -------------------- Eliminar testimonio (ADMIN) --------------------
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def eliminar_testimonio_admin(request, id):
    testimonio = get_object_or_404(TestimonioVerificado, id=id)

    if request.method == 'POST':
        testimonio.delete()
        messages.success(request, f"Testimonio '{testimonio.titulo}' eliminado.")
        return redirect('testimonios')

    return render(request, 'formularios/confirmar_eliminar.html', {'testimonio': testimonio})


# -------------------- Eliminar testimonio (DUEÑO) --------------------
def eliminar_testimonio_dueno(request, id):
    testimonio = get_object_or_404(TestimonioVerificado, id=id)

    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión.")
        return redirect('login')

    try:
        usuario_rut = request.user.profile.rut
    except Profile.DoesNotExist:
        messages.error(request, "Tu perfil no tiene RUT.")
        return redirect('testimonios')

    if usuario_rut != testimonio.rut:
        messages.error(request, "No tienes permiso.")
        return redirect('testimonios')

    if request.method == 'POST':
        testimonio.delete()
        messages.success(request, "Testimonio eliminado.")
        return redirect('testimonios')

    return render(request, 'formularios/confirmar_eliminar.html', {'testimonio': testimonio})


# -------------------- FUNDACIONES --------------------
def fundaciones(request):

    fundaciones_aprobadas = FundacionPropuesta.objects.filter(aprobada=True)


    fundaciones_pendientes = None
    if request.user.is_authenticated and (
        request.user.is_superuser or
        request.user.is_staff or
        request.user.groups.filter(name='Administradores').exists()
    ):
        fundaciones_pendientes = FundacionPropuesta.objects.filter(aprobada=False)

    return render(request, 'fundaciones.html', {
        'fundaciones_aprobadas': fundaciones_aprobadas,  
        'fundaciones_pendientes': fundaciones_pendientes,
    })
@user_passes_test(lambda u: u.is_superuser or u.is_staff or u.groups.filter(name='Administradores').exists())
def aprobar_fundacion(request, id):
    fundacion = get_object_or_404(FundacionPropuesta, id=id)
    fundacion.aprobada = True
    fundacion.save()
    messages.success(request, "Fundación aprobada correctamente.")
    return redirect('fundaciones')

@user_passes_test(lambda u: u.is_superuser or u.is_staff or u.groups.filter(name='Administradores').exists())
def rechazar_fundacion(request, id):
    fundacion = get_object_or_404(FundacionPropuesta, id=id)
    fundacion.delete()
    messages.success(request, "Fundación eliminada correctamente.")
    return redirect('fundaciones')
@user_passes_test(lambda u: u.is_superuser or u.is_staff or u.groups.filter(name='Administradores').exists())
def eliminar_fundacion_aprobada(request, id):
    fundacion = get_object_or_404(FundacionPropuesta, id=id, aprobada=True)
    fundacion.delete()
    messages.success(request, "Fundación aprobada eliminada correctamente.")
    return redirect('fundaciones')
def fundaciones(request):
    fundaciones_publicas = FundacionPropuesta.objects.filter(aprobada=True)

    fundaciones_pendientes = None
    if request.user.is_authenticated and (
        request.user.is_superuser or 
        request.user.is_staff or 
        request.user.groups.filter(name='Administradores').exists()
    ):
        fundaciones_pendientes = FundacionPropuesta.objects.filter(aprobada=False)

    # 🔥 PASAR VARIABLE PARA SABER SI ES ADMIN
    es_admin = False
    if request.user.is_authenticated:
        es_admin = (
            request.user.is_superuser or
            request.user.is_staff or 
            request.user.groups.filter(name='Administradores').exists()
        )

    return render(request, 'fundaciones.html', {
        'fundaciones_aprobadas': fundaciones_publicas,
        'fundaciones_pendientes': fundaciones_pendientes,
        'es_admin': (
            request.user.is_authenticated and 
            (request.user.is_staff or request.user.is_superuser or 
            request.user.groups.filter(name='Administradores').exists())
        )
    })

# -------------------- Crear fundación (usuario) --------------------

# -------------------- Aprobar Fundación (ADMIN) --------------------
@user_passes_test(lambda u: u.is_staff or u.is_superuser or u.groups.filter(name='Administradores').exists())
def aprobar_fundacion(request, id):
    fundacion = get_object_or_404(FundacionPropuesta, id=id)
    fundacion.aprobada = True
    fundacion.save()
    messages.success(request, "Fundación aprobada y ahora visible al público.")
    return redirect('fundaciones')

def crear_fundacion(request):

    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para añadir una fundación.")
        return redirect('login')

    if request.method == 'POST':
        form = FundacionPropuestaForm(request.POST, request.FILES)
        if form.is_valid():

            nueva = form.save(commit=False)

            nueva.usuario = request.user
            nueva.aprobada = False

            #  Guardar geolocalización correctamente
            nueva.lat = request.POST.get('latitud')
            nueva.lng = request.POST.get('longitud')

            #  Guardar redes sociales del HTML
            nueva.instagram = request.POST.get('instagram')
            nueva.facebook = request.POST.get('facebook')
            nueva.tiktok = request.POST.get('tiktok')
            nueva.twitter = request.POST.get('twitter')

            nueva.save()

            messages.success(request, "Fundación enviada. Un administrador debe aprobarla.")
            return redirect('fundaciones')

    else:
        form = FundacionPropuestaForm()

    return render(request, 'formularios/fundacion_form.html', {'form': form})

# -------------------- Eliminar Fundación (ADMIN) --------------------
@user_passes_test(lambda u: u.is_staff or u.is_superuser or u.groups.filter(name='Administradores').exists())
def eliminar_fundacion(request, id):
    fundacion = get_object_or_404(FundacionPropuesta, id=id)
    fundacion.delete()
    messages.success(request, "Fundación eliminada correctamente.")
    return redirect('fundaciones')


# -------------------- CONTACTO --------------------
def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Mensaje enviado correctamente.")
            return redirect('contacto')
        messages.error(request, "Revisa los errores.")
    else:
        form = ContactoForm()

    mensajes_contacto = None
    if request.user.is_authenticated and (
        request.user.is_superuser or
        request.user.is_staff or
        request.user.groups.filter(name='Administradores').exists()
    ):
        mensajes_contacto = MensajeContacto.objects.all()

    return render(request, 'contacto.html', {
        'form': form,
        'mensajes_contacto': mensajes_contacto
    })


# -------------------- Eliminar mensaje contacto (ADMIN) --------------------
@user_passes_test(lambda u: u.is_superuser or u.is_staff or u.groups.filter(name='Administradores').exists())
def eliminar_mensaje_contacto(request, id):
    mensaje = get_object_or_404(MensajeContacto, id=id)
    mensaje.delete()
    messages.success(request, "Mensaje eliminado correctamente.")
    return redirect('contacto')


# -------------------- Login --------------------
def login_view(request):

    storage = messages.get_messages(request)
    for _ in storage:
        pass

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Bienvenido.")
            return redirect('inicio')
        messages.error(request, "Credenciales incorrectas.")
    else:
        form = AuthenticationForm()

    return render(request, 'formularios/login.html', {'form': form})


# -------------------- Registro Usuario --------------------
def registro_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            try:
                usuarios_group = Group.objects.get(name='Usuarios')
                user.groups.add(usuarios_group)
            except Group.DoesNotExist:
                pass

            messages.success(request, "Cuenta creada.")
            return redirect('login')
        messages.error(request, "Errores en el formulario.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'formularios/registro_usuario.html', {'form': form})


# -------------------- Logout --------------------
def custom_logout_view(request):
    logout(request)
    messages.success(request, "Sesión cerrada.")
    return redirect('inicio')


# -------------------- API REST --------------------
from django.http import JsonResponse

def api_fundaciones(request):
    fundaciones = FundacionPropuesta.objects.filter(aprobada=True).values(
        'id',
        'nombre',
        'descripcion',
        'lat',
        'lng'
    )
    return JsonResponse(list(fundaciones), safe=False)
