from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver

# -------------------- Profile --------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=12, unique=True, blank=True, null=True) 

    def __str__(self):
        return f'Perfil de {self.user.username}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
    instance.profile.save()


# -------------------- Usuario (No usado para Auth) --------------------
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre_completo = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usuarios'

    def __str__(self):
        return self.nombre_completo


# -------------------- Testimonio --------------------
class Testimonio(models.Model):
    id_testimonio = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    titulo = models.CharField(max_length=150)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=False)

    class Meta:
        db_table = 'testimonios'

    def __str__(self):
        return self.titulo


# -------------------- Centro Médico --------------------
class CentroMedico(models.Model):
    id_centro = models.AutoField(primary_key=True)
    nombre_centro = models.CharField(max_length=150)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    contacto = models.CharField(max_length=100, blank=True, null=True)
    sitio_web = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'centros_medicos'

    def __str__(self):
        return self.nombre_centro


# -------------------- Médico --------------------
class Medico(models.Model):
    id_medico = models.AutoField(primary_key=True)
    nombre_medico = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    id_centro = models.ForeignKey(CentroMedico, on_delete=models.SET_NULL, null=True, db_column='id_centro')

    class Meta:
        db_table = 'medicos'

    def __str__(self):
        return self.nombre_medico


# -------------------- Fundación --------------------
class Fundacion(models.Model):
    id_fundacion = models.AutoField(primary_key=True)
    nombre_fundacion = models.CharField(max_length=150)
    region = models.CharField(max_length=100, blank=True, null=True)
    contacto = models.CharField(max_length=100, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    sitio_web = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'fundaciones'

    def __str__(self):
        return self.nombre_fundacion


# -------------------- Contenido informativo --------------------
class ContenidoInformativo(models.Model):
    id_contenido = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    autor = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'contenidos_informativos'

    def __str__(self):
        return self.titulo


# -------------------- Testimonio Verificado --------------------
class TestimonioVerificado(models.Model):
    titulo = models.CharField(max_length=150)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, blank=True, null=True)
    correo = models.EmailField()
    rut = models.CharField(max_length=12)
    mostrar_nombre = models.BooleanField(default=True)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'testimonios_verificados'

    def nombre_publico(self):
        if self.mostrar_nombre:
            return f"{self.nombre} {self.apellido or ''}".strip()
        return "Anónimo"

    def __str__(self):
        return f"{self.titulo} - {self.nombre_publico()}"


# -------------------- Mensajes de Contacto --------------------
class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=150)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    class Meta:
        db_table = 'mensajes_contacto'

    def __str__(self):
        return f"{self.nombre} - {self.email}"
# -------------------- Fundaciones Propuestas por Usuarios --------------------
class FundacionPropuesta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    ubicacion = models.CharField(max_length=150)

    instagram = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    tiktok = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)

    sitio_web = models.URLField(blank=True, null=True)

    icono = models.ImageField(upload_to='fundaciones_iconos/', blank=True, null=True)

    aprobada = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'fundaciones_propuestas'

    def __str__(self):
        return self.nombre
