import os
import sys
import site
from django.core.wsgi import get_wsgi_application

sys.path.append('C:/Users/Administrator/Desktop/sdndefender/dashboard')
os.environ['DJANGO_SETTINGS_MODULE'] = 'sdndefender.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdndefender.settings')
application = get_wsgi_application()