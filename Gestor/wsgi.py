"""
WSGI config for aguas_del_valle project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aguas_del_valle.settings')

application = get_wsgi_application()
