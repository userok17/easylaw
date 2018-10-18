#!/home/easylaw/myenv/bin/python3
import os, sys
sys.path.insert(0, os.path.join(os.path.expanduser('~'), 'projects/blank/blank'))
sys.path.insert(0, os.path.join(os.path.expanduser('~'), 'projects/blank'))

sys.path.insert(0, '/home/easylaw/myenv/lib/python3.4/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'blank.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
