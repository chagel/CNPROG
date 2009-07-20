# encoding:utf-8
SITE_SRC_ROOT = '/change_me/'

#for logging
import logging
LOG_FILENAME = SITE_SRC_ROOT + 'django.lanai.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)

DATABASE_NAME = 'cnprog'             # Or path to database file if using sqlite3.
DATABASE_USER = 'root'               # Not used with sqlite3.
DATABASE_PASSWORD = ''               # Not used with sqlite3.

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)
