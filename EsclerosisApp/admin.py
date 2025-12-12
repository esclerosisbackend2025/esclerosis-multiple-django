from django.contrib import admin
from .models import (
    Usuario, Testimonio, TestimonioVerificado,
    CentroMedico, Medico, Fundacion, ContenidoInformativo
)

# -------------------- Registro general --------------------
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'email', 'fecha_registro')
    search_fields = ('nombre_completo', 'email')


@admin.register(CentroMedico)
class CentroMedicoAdmin(admin.ModelAdmin):
    list_display = ('nombre_centro', 'region', 'contacto')
    search_fields = ('nombre_centro', 'region')


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nombre_medico', 'especialidad', 'id_centro')
    search_fields = ('nombre_medico', 'especialidad')


@admin.register(Fundacion)
class FundacionAdmin(admin.ModelAdmin):
    list_display = ('nombre_fundacion', 'region', 'correo')
    search_fields = ('nombre_fundacion', 'region')


@admin.register(ContenidoInformativo)
class ContenidoInformativoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'fecha_publicacion')
    search_fields = ('titulo', 'autor')


# -------------------- Testimonios verificados --------------------
@admin.register(TestimonioVerificado)
class TestimonioVerificadoAdmin(admin.ModelAdmin):
    list_display = ('nombre_publico', 'correo', 'fecha_envio', 'aprobado')
    list_filter = ('aprobado', 'fecha_envio')
    search_fields = ('nombre', 'apellido', 'correo', 'mensaje')
    list_editable = ('aprobado',)
    ordering = ('-fecha_envio',)
    readonly_fields = ('fecha_envio',)

    # --- Acción personalizada: aprobar varios testimonios ---
    actions = ['aprobar_testimonios']

    def aprobar_testimonios(self, request, queryset):
        count = queryset.update(aprobado=True)
        self.message_user(request, f"{count} testimonio(s) fueron aprobados correctamente.")
    aprobar_testimonios.short_description = "Aprobar testimonios seleccionados"

    # --- Asegurar que la opción eliminar esté disponible ---
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' not in actions:
            from django.contrib.admin.actions import delete_selected
            actions['delete_selected'] = (
                delete_selected,
                'delete_selected',
                'Eliminar testimonios seleccionados'
            )
        return actions
