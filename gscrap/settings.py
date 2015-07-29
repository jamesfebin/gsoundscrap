"""
Django settings for gscrap project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import dj_database_url

DEFAULT_DB = "postgres://localhost"

DATABASES = {'default': dj_database_url.config(default=DEFAULT_DB)}
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']
import os

db_url = os.environ.get("DATABASE_URL", DEFAULT_DB)

DEFAULT_AMQP = "amqp://guest:guest@localhost//"
app = Celery("tasks", backend=db_url.replace("postgres://", "db+postgresql://"),
             broker=os.environ.get("CLOUDAMQP_URL", DEFAULT_AMQP))
app.BROKER_POOL_LIMIT = 1


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2c&#zz9m)c=lxvb73=i8i#b&ie&pl&mr6^_1qfq$kvxn(zfa-^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'gscrapweb',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'gscrap.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'gscrap.wsgi.application'


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "380183775330-a93oui632sm6vmmurrn5ptbe239ml599.apps.googleusercontent.com"

SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "kMMLbJ7z3x9xOft5MGynaou3"

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE=["https://www.googleapis.com/auth/youtube","https://www.googleapis.com/auth/gmail.readonly"]


SOCIAL_AUTH_SOUNDCLOUD_KEY = "2e45f18b4dd8d3a67abebfa6c79ad8e0"

SOCIAL_AUTH_SOUNDCLOUD_SECRET = "4280bf11630a91413fba77222f3f8005"


AUTH_USER_MODEL = "gscrapweb.CustomUser"


GOOGLE_OAUTH2_USE_UNIQUE_USER_ID = True

SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
    'access_type': 'offline',
    'approval_prompt': 'force'
}

AUTHENTICATION_BACKENDS = (
   'social.backends.google.GoogleOAuth2',
    'social.backends.soundcloud.SoundcloudOAuth2',
    'django.contrib.auth.backends.ModelBackend'

)



# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/


STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "public","production")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "public","assets"),
    #'/var/www/static/',
)
