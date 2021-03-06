# Django settings for hcm_p project.
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


DEBUG = True
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',       # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_ROOT, 'db'),     # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT, '../locale'),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, '../media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, '../static/'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ttne7w--=o_2je1md1c*rh9p=$o17h(=l1ut*fr3_s=bf5c6x='

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'pybb.middleware.PybbMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'pybb.context_processors.processor',
    'postman.context_processors.inbox',
)

ROOT_URLCONF = 'hcm.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'hcm.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, '../templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'south',
    'sorl.thumbnail',  # uses in imagestore, pybb
    'pure_pagination',
    'django_forms_bootstrap',
    'pinax_theme_bootstrap',
    'guardian',  # uses in userena
    'easy_thumbnails',  # uses in userena
    'tagging',
    'notification',  # uses in postman
    'ajax_select',  # uses in postman, imagestore
    'unidecode',  # uses for slugify unicode strings
    'honeypot',  # uses for hcm_blog to prevent spam
    'markitup',  # uses for hcm_blog editor
    # 'mailer',  # include for production

    'userena',  # sign in/sign up app
    'postman',  # messages app
    'pybb',  # forum app
    'imagestore',  # albums app
    'hcm',  # hcm core app
    'hcm_news',  # hcm news app
    'hcm_blog',  # hcm blog app
    'hcm_profile',  # hcm profile app
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

LOGIN_URL = '/accounts/signin/'

AUTH_PROFILE_MODULE = 'hcm_profile.MainUserProfile'

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_REDIRECT_URL = '/hcm_profile/%(username)s/'
LOGIN_URL = '/hcm_profile/signin/'
LOGOUT_URL = '/hcm_profilec/signout/'

ANONYMOUS_USER_ID = -1

USERENA_PROFILE_DETAIL_TEMPLATE = 'profile_detail.html'

PYBB_PROFILE_RELATED_NAME = 'hcm_profile'
PYBB_TEMPLATE = 'forum_base.html'


AJAX_LOOKUP_CHANNELS = {
    'user': ('hcm_profile.lookups', 'UserLookup'),
    'tag': {'model': 'tagging.Tag', 'search_field': 'name'}
}
AJAX_SELECT_BOOTSTRAP = False
AJAX_SELECT_INLINES = 'staticfiles'

IMAGESTORE_IMAGE_FORM = 'hcm.forms.HcmImageForm'

POSTMAN_DISALLOW_ANONYMOUS = True
POSTMAN_DISABLE_USER_EMAILING = True
POSTMAN_AUTO_MODERATE_AS = True
POSTMAN_AUTOCOMPLETER_APP = {
    'arg_default': 'user'
}

HONEYPOT_FIELD_NAME = 'comment_body'

JQUERY_URL = None
MARKITUP_SET = 'markitup/sets/markdown'
MARKITUP_FILTER = ('markdown.markdown', {'safe_mode': 'remove', 'html_replacement_text': ''})

try:
    from settings_local import *
except ImportError:
    pass