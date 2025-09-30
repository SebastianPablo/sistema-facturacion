"""
Configuración avanzada de base de datos con conexiones seguras.
"""

import os
from decouple import config

def get_database_config():
    """Obtener configuración de base de datos según el entorno."""
    environment = config('ENVIRONMENT', default='development')
    
    if environment == 'production':
        return {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
            'OPTIONS': {
                'sslmode': 'require',
                'connect_timeout': 10,
                'options': '-c default_transaction_isolation=read_committed'
            },
            'CONN_MAX_AGE': 60,  # Pool de conexiones
            'CONN_HEALTH_CHECKS': True,
        }
    else:
        # Desarrollo - SQLite
        return {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(os.path.dirname(__file__), '..', 'db.sqlite3'),
        }

def get_cache_config():
    """Configuración de cache para optimización."""
    return {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': config('REDIS_URL', default='redis://127.0.0.1:6379/1'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            },
            'KEY_PREFIX': 'facturacion',
            'TIMEOUT': 300,  # 5 minutos
        }
    }

def get_session_config():
    """Configuración de sesiones seguras."""
    return {
        'SESSION_ENGINE': 'django.contrib.sessions.backends.cache',
        'SESSION_CACHE_ALIAS': 'default',
        'SESSION_COOKIE_AGE': 3600,  # 1 hora
        'SESSION_EXPIRE_AT_BROWSER_CLOSE': True,
        'SESSION_COOKIE_SECURE': config('SESSION_COOKIE_SECURE', default=False, cast=bool),
        'SESSION_COOKIE_HTTPONLY': True,
        'SESSION_COOKIE_SAMESITE': 'Lax',
    }
