import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aguas_del_valle.settings')

application = get_asgi_application()
