# encoding:utf-8
# Django settings for lanai project.
import os.path

#DEBUG SETTINGS
DEBUG = True
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ('127.0.0.1',)

#for OpenID auth
ugettext = lambda s: s
LOGIN_URL = '/%s%s' % (ugettext('account/'), ugettext('signin/'))

#EMAIL AND ADMINS
ADMINS = (
    ('CNProg team', 'team@cnprog.com'),
)
MANAGERS = ADMINS

SITE_ID = 1

ADMIN_MEDIA_PREFIX = '/admin/media/'
SECRET_KEY = '$oo^&_m&qwbib=(_4m_n*zn-d=g#s0he5fx9xonnym#8p6yigm'
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    #'django.middleware.sqlprint.SqlPrintingMiddleware',
    #'middleware.pagesize.QuestionsPageSizeMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'context.auth_processor',
    'context.application_settings',
    #'django.core.context_processors.i18n',
    'django.core.context_processors.auth' #this is required for admin
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
)

#UPLOAD SETTINGS
FILE_UPLOAD_TEMP_DIR = os.path.join(os.path.dirname(__file__), 'tmp').replace('\\','/')
FILE_UPLOAD_HANDLERS = ("django.core.files.uploadhandler.MemoryFileUploadHandler",
 "django.core.files.uploadhandler.TemporaryFileUploadHandler",)
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
# for user upload
ALLOW_FILE_TYPES = ('.jpg', '.jpeg', '.gif', '.bmp', '.png', '.tiff')
# unit byte
ALLOW_MAX_FILE_SIZE = 1024 * 1024

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.humanize',
    'forum',
    'django_authopenid',
    #'debug_toolbar' ,
)
import django
DJANGO_VERSION = django.get_version()
# User settings
from settings_local import *