"""
Django settings for Proyecto_Esclerosis project.
"""
"""
Configuración principal de Django para el proyecto Esclerosis Múltiple.
"""

from pathlib import Path
import os

# --- Configuración base ---
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-%xp&ai76wwhpd@v#ewk9q73y+9q+&j(j#2k*(7#a^odp3o=%34'
DEBUG = False
ALLOWED_HOSTS = [
    'esclerosis-multiple-django.onrender.com',
    'localhost',
    '127.0.0.1',
]

# --- Aplicaciones instaladas ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'EsclerosisApp.apps.EsclerosisappConfig',
]

# --- Middleware ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Proyecto_Esclerosis.urls'

# --- Configuración de templates ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'EsclerosisApp', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Proyecto_Esclerosis.wsgi.application'

# --- Base de datos ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- Validación de contraseñas ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Localización ---
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# --- Archivos estáticos ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "EsclerosisApp" / "static"]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# :fire: ESTA ES LA ÚNICA LÍNEA NUEVA (NO TOCA NADA MÁS)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Configuración de correo (SMTP Gmail) ---
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "esclerosisbackend2025@gmail.com"
EMAIL_HOST_PASSWORD = "aenwrggiphntahxh"  # contraseña de aplicación
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

#--Login redireccion--
LOGIN_REDIRECT_URL = 'inicio'
ADMIN_REGISTRATION_KEY = 'Esclerosis@dmin2025'

# --- Archivos Multimedia (para imágenes subidas por usuarios) ---
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
