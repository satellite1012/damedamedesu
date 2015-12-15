"""
WSGI config for sogi project.
"""

from django.core.wsgi import get_wsgi_application
from dj_static import Cling
from django.conf import settings

application = Cling(get_wsgi_application())

if not settings.configured:
    settings.configure()
    
