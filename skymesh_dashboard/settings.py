"""
Django settings for skymesh_dashboard project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cyu0)hbs%47(cgth_lya9j_p1%ah(1i^t%x7b+8hex@!vd75a_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'dome',
    'kiwi',
    'acorn',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'skymesh_dashboard.urls'

WSGI_APPLICATION = 'skymesh_dashboard.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(BASE_DIR, 'dome.sqlite3'),                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'media'))
MEDIA_URL = '/media/'
# STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'static'))
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # os.path.join(
    #     os.path.dirname(__file__),
    #     'static',
    # ),

    os.path.join(BASE_DIR, "static"),
)

#SOCIAL_AUTH_LOGIN_URL = '/auth/login/'
LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/'
# SOCIAL_AUTH_USERNAME_FORM_URL = '/signup-username'
SOCIAL_AUTH_USERNAME_FORM_HTML = 'acorn/username_signup.html'

AUTHENTICATION_BACKENDS = (
  'social.backends.open_id.OpenIdAuth',
  'social.backends.google.GoogleOpenId',
  'social.backends.google.GoogleOAuth2',
  'social.backends.google.GoogleOAuth',
  'social.backends.dropbox.DropboxOAuth2',
  'social.backends.username.UsernameAuth',

  'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '263593193734-8gf5o4rn7c4litg0gqk5f9u5vfbqv310.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'JEotJtmMkGRmZRqU9eothCyD'