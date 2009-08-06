import os
import sys

sys.path.append('/var/www/vhosts')
os.environ['DJANGO_SETTINGS_MODULE'] = 'cnprog.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
