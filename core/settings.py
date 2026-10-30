"""Django settings for the EcoTech project."""

import os
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'local-development-key-please-set-secret-key-in-production-2026',
)
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = [host.strip() for host in os.getenv(
    'ALLOWED_HOSTS',
    'localhost,127.0.0.1,.vercel.app',
).split(',') if host.strip()]
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in os.getenv(
    'CSRF_TRUSTED_ORIGINS',
    'https://*.vercel.app,http://localhost:8000,http://127.0.0.1:8000',
).split(',') if origin.strip()]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ecotech',
]

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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    try:
        import dj_database_url
    except ImportError:
        parsed_db = urlparse(DATABASE_URL)
        if parsed_db.scheme in ('sqlite', 'sqlite3'):
            DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}
        else:
            DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql', 'NAME': parsed_db.path.lstrip('/'), 'USER': parsed_db.username, 'PASSWORD': parsed_db.password, 'HOST': parsed_db.hostname, 'PORT': parsed_db.port or 5432}}
    else:
        DATABASES = {'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
else:
    db_database = os.getenv('database') or os.getenv('DB_NAME')
    if db_database:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': db_database,
                'USER': os.getenv('user') or os.getenv('DB_USER'),
                'PASSWORD': os.getenv('password') or os.getenv('DB_PASSWORD'),
                'HOST': os.getenv('host') or os.getenv('DB_HOST'),
                'PORT': os.getenv('port') or os.getenv('DB_PORT'),
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': BASE_DIR / 'db.postgres',  # Default to a local SQLite database for development
            }
        }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles_build'
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = not DEBUG
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

MAILERS = {
    'default': {
        'BACKEND': os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend'),
        'HOST': os.getenv('EMAIL_HOST', ''),
        'PORT': os.getenv('EMAIL_PORT', '587'),
        'USERNAME': os.getenv('EMAIL_HOST_USER', ''),
        'PASSWORD': os.getenv('EMAIL_HOST_PASSWORD', ''),
        'USE_TLS': os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true',
    },
}
