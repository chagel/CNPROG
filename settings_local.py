# encoding:utf-8

#path must have slash appended!!!
SITE_SRC_ROOT = '/var/www/vhosts/default/htdocs/cnprog-tests/test/'
LOG_FILENAME = 'django.lanai.log'

#for logging
import logging
logging.basicConfig(filename=SITE_SRC_ROOT + 'log/' + LOG_FILENAME, level=logging.DEBUG,)

DATABASE_NAME = 'cnprog'             # Or path to database file if using sqlite3.
DATABASE_USER = 'cnprog'               # Not used with sqlite3.
DATABASE_PASSWORD = ''               # Not used with sqlite3.
DATABASE_ENGINE = ''  #mysql, etc

#why does this stuff go here?
#MIDDLEWARE_CLASSES = (
#    'django.middleware.gzip.GZipMiddleware',
#    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.locale.LocaleMiddleware',
#    'django.middleware.common.CommonMiddleware',
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.middleware.transaction.TransactionMiddleware',
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
#)
