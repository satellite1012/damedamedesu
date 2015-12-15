"""
WSGI config for sogi project.
"""

from django.core.wsgi import get_wsgi_application
from dj_static import Cling
    
application = Cling(get_wsgi_application())

