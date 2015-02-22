import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from .secrets import SECRET_KEY

DEBUG = False
TEMPLATE_DEBUG = DEBUG
ROOT_URLCONF = 'mjapp.urls'
TIME_ZONE = 'UTC'
USE_I18N = False
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

ALLOWED_HOSTS = (
    'mahjong.maxb.eu',
    'xn--8n5a30n.maxb.eu',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'stats',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)
