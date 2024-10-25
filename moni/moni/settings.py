"""
Django settings for moni project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path  # Importa Path para manejar rutas de archivos y directorios
import os  # Importa os para interactuar con el sistema operativo

# Construye rutas dentro del proyecto como BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración de inicio rápido para desarrollo - no apta para producción
# Ver https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# ADVERTENCIA DE SEGURIDAD: mantén la clave secreta usada en producción en secreto!
SECRET_KEY = 'django-insecure-lxw&6j4r!nw6^et0g44xn#&anc3l&v@_f*n*#&&_rj5mxnhqx)'

# ADVERTENCIA DE SEGURIDAD: no ejecutes con debug activado en producción!
DEBUG = True

ALLOWED_HOSTS = ['*']  # Permite todas las conexiones de host

# Definición de la aplicación

INSTALLED_APPS = [
    'rest_framework' , # Aplicación de REST Framework
    'rest_framework.authtoken',# Para autenticación basada en tokens
    'rest_framework_simplejwt', # Para autenticación basada en JWT (JSON Web Token) para la API
    'django.contrib.admin',  # Aplicación de administración de Django
    'django.contrib.auth',  # Aplicación de autenticación de Django
    'django.contrib.contenttypes',  # Aplicación de tipos de contenido de Django
    'django.contrib.sessions',  # Aplicación de sesiones de Django
    'django.contrib.messages',  # Aplicación de mensajes de Django
    'django.contrib.staticfiles',  # Aplicación de archivos estáticos de Django
    # APPS
    'api',
    'crud',  # Aplicación personalizada 'crud'
    'nucleo',  # Aplicación personalizada 'nucleo'
    'user',  # Aplicación personalizada 'user'
    'evaluacion',  # Aplicación personalizada 'evaluacion'
    'habitantes',  # Aplicación personalizada 'habitantes'
]

# Configuración de Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

MIDDLEWARE = [
    # No Borrar
    'mqtt_data.middleware.MQTTMiddleware',  # Middleware personalizado para MQTT
    ###

    'django.middleware.security.SecurityMiddleware',  # Middleware de seguridad de Django
    'django.contrib.sessions.middleware.SessionMiddleware',  # Middleware de sesiones de Django
    'django.middleware.common.CommonMiddleware',  # Middleware común de Django
    'django.middleware.csrf.CsrfViewMiddleware',  # Middleware de protección CSRF de Django
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Middleware de autenticación de Django
    'django.contrib.messages.middleware.MessageMiddleware',  # Middleware de mensajes de Django
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Middleware de protección contra clickjacking de Django
]

ROOT_URLCONF = 'moni.urls'  # Configuración de la raíz de URLs

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Backend de plantillas de Django
        'DIRS': [
            os.path.join(BASE_DIR, 'frontend', 'templates'),  # Directorio de plantillas del frontend
            os.path.join(BASE_DIR, 'moni', 'habitantes', 'templates'),  # Directorio de plantillas de la aplicación 'habitantes'
        ],
        'APP_DIRS': True,  # Habilita la búsqueda de plantillas en los directorios de las aplicaciones
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # Procesador de contexto para depuración
                'django.template.context_processors.request',  # Procesador de contexto para la solicitud
                'django.contrib.auth.context_processors.auth',  # Procesador de contexto para autenticación
                'django.contrib.messages.context_processors.messages',  # Procesador de contexto para mensajes
            ],
        },
    },
]

WSGI_APPLICATION = 'moni.wsgi.application'  # Configuración de la aplicación WSGI

# Base de datos
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",  # Motor de base de datos PostgreSQL
        "NAME": "AquaCircuitBD",  # Nombre de la base de datos
        "USER": "postgres",  # Usuario de la base de datos
        "PASSWORD": "Eduardo1",  # Contraseña de la base de datos
        "HOST": "localhost",  # Host de la base de datos
        "PORT": "5432",  # Puerto de la base de datos
    }
}

# Validación de contraseñas
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # Validador de similitud de atributos de usuario
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # Validador de longitud mínima
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # Validador de contraseñas comunes
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # Validador de contraseñas numéricas
    },
]

# Internacionalización
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es-cl'  # Código de idioma
TIME_ZONE = 'UTC'  # Zona horaria
USE_I18N = True  # Habilita la internacionalización
USE_TZ = True  # Habilita el uso de zonas horarias

# Archivos estáticos (CSS, JavaScript, Imágenes)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'  # URL para archivos estáticos

# Directorios de archivos estáticos
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),  # Directorio de archivos estáticos
]

# Tipo de campo de clave primaria predeterminado
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Tipo de campo de clave primaria predeterminado
AUTH_USER_MODEL = 'user.User'  # Modelo de usuario personalizado
LOGIN_URL = 'nucleo:login'  # URL de inicio de sesión
LOGIN_REDIRECT_URL = 'nucleo:revision'  # URL de redirección después de iniciar sesión
LOGOUT_REDIRECT_URL = 'nucleo:login'  # URL de redirección después de cerrar sesión

# Configuración de correo electrónico
EMAIL_HOST = 'smtp.gmail.com'  # Host del servidor de correo electrónico
EMAIL_PORT = 587  # Puerto del servidor de correo electrónico
EMAIL_HOST_USER = 'c.quilodran.ignacio@gmail.com'  # Usuario del servidor de correo electrónico
EMAIL_HOST_PASSWORD = 'hwcy cywn xohv wdtt'  # Contraseña del servidor de correo electrónico

DOMAIN = ''  # Dominio del proyecto