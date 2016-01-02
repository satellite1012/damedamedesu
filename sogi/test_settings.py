from sogi.settings import *

# faster tests with in-memory sqlite3
SOUTH_TESTS_MIGRATE = False
DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}
