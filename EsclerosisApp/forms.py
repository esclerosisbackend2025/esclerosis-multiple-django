from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from itertools import cycle
from django.conf import settings
from .models import (
    TestimonioVerificado,
    Profile,
    MensajeContacto,
    FundacionPropuesta
)
import re

# -------------------- Validación RUT --------------------
def validar_rut(rut):
    rut = rut.replace(".", "").replace(" ", "").upper()

    if "-" not in rut:
        rut = rut[:-1] + "-" + rut[-1]

    if not re.match(r"^\d{7,8}-[\dK]$", rut):
        return False

    cuerpo, dv_ingresado = rut.split("-")
    revertido = map(int, reversed(cuerpo))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(revertido, factors))
    mod = 11 - (s % 11)
    dv_esperado = "K" if mod == 10 else "0" if mod == 11 else str(mod)

    return dv_ingresado == dv_esperado


# -------------------- Registro usuario normal --------------------
class CustomUserCreationForm(UserCreationForm):
    rut = forms.CharField(
        label="RUT (Ej: 12.345.678-K)",
        max_length=12,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RUT'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('rut', 'email',)

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if not validar_rut(rut):
            raise forms.ValidationError("El RUT ingresado no es válido.")

        normalized_rut = rut.replace(".", "").replace(" ", "").upper()
        if self.instance.pk is None and Profile.objects.filter(rut=normalized_rut).exists():
            raise forms.ValidationError("Ya existe una cuenta registrada con este RUT.")
        return normalized_rut

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user.profile.rut = self.cleaned_data['rut']
            user.profile.save()
        return user


# -------------------- Registro Admin --------------------
class RegistroAdminForm(CustomUserCreationForm):
    admin_key = forms.CharField(
        label="Clave Secreta de Administrador",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta(CustomUserCreationForm.Meta):
        fields = CustomUserCreationForm.Meta.fields + ('admin_key',)

    def clean_admin_key(self):
        key = self.cleaned_data.get('admin_key')
        expected = getattr(settings, 'ADMIN_REGISTRATION_KEY', None)

        if not expected:
            raise forms.ValidationError("Falta ADMIN_REGISTRATION_KEY en settings.py.")
        if key != expected:
            raise forms.ValidationError("Clave Secreta incorrecta.")
        return key

    def save(self, commit=True):
        user = super().save(commit=False)

        # MARCAR COMO ADMIN REAL
        user.is_staff = True
        user.is_superuser = True

        if commit:
            user.save()

            # Crear o recuperar grupo Administradores
            from django.contrib.auth.models import Group
            grupo, created = Group.objects.get_or_create(name="Administradores")

            # Agregar usuario al grupo
            user.groups.add(grupo)

        return user

# -------------------- Testimonio --------------------
class TestimonioVerificadoForm(forms.ModelForm):
    class Meta:
        model = TestimonioVerificado
        fields = ['titulo', 'nombre', 'apellido', 'correo', 'rut', 'mostrar_nombre', 'mensaje']

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'mostrar_nombre': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if not validar_rut(rut):
            raise forms.ValidationError("RUT no válido.")
        return rut.replace(".", "").replace(" ", "").upper()


# -------------------- Verificar Rut --------------------
class VerificarRutForm(forms.Form):
    rut = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: 12.345.678-K'})
    )

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if not validar_rut(rut):
            raise forms.ValidationError("RUT no válido.")
        return rut.replace(".", "").replace(" ", "").upper()


# -------------------- Contacto --------------------
class ContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'mensaje']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'contacto-input'}),
            'email': forms.EmailInput(attrs={'class': 'contacto-input'}),
            'mensaje': forms.Textarea(attrs={'class': 'contacto-input contacto-textarea'}),
        }


# ============================================================
# FORMULARIO FUNDACIÓN PROPUESTA
# ============================================================
class FundacionPropuestaForm(forms.ModelForm):
    class Meta:
        model = FundacionPropuesta
        fields = [
            'nombre',
            'descripcion',
            'ubicacion',
            'instagram',
            'facebook',
            'tiktok',
            'twitter',
            'sitio_web',
            'icono',
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'contacto-input'}),
            'descripcion': forms.Textarea(attrs={'class': 'contacto-input', 'rows': 3}),
            'ubicacion': forms.TextInput(attrs={'class': 'contacto-input'}),
            'instagram': forms.TextInput(attrs={'class': 'contacto-input'}),
            'facebook': forms.TextInput(attrs={'class': 'contacto-input'}),
            'tiktok': forms.TextInput(attrs={'class': 'contacto-input'}),
            'twitter': forms.TextInput(attrs={'class': 'contacto-input'}),
            'sitio_web': forms.URLInput(attrs={'class': 'contacto-input'}),
            'icono': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


    def clean_icono(self):
        icono = self.cleaned_data.get('icono')
        if not icono:
            raise forms.ValidationError("Debes subir un logo para la fundación.")
        return icono
