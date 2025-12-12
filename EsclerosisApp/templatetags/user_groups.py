# EsclerosisApp/templatetags/user_groups.py

from django import template
# No es estrictamente necesario importar Group, pero es bueno si se necesita en el futuro
# from django.contrib.auth.models import Group 

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Verifica si el usuario pertenece al grupo especificado
    """
    if user.is_authenticated:
        # Nota: El atributo 'groups' ya está disponible en el objeto User
        return user.groups.filter(name=group_name).exists()
    return False

# Si usaste un IDE o editor, asegúrate de que no haya caracteres extraños o errores tipográficos (typos).