"""
Middleware personalizado para seguridad adicional.
"""

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Middleware para agregar headers de seguridad adicionales.
    """
    
    def process_response(self, request, response):
        # Headers de seguridad
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # Content Security Policy
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https:; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        response['Content-Security-Policy'] = csp
        
        return response


class RateLimitMiddleware(MiddlewareMixin):
    """
    Middleware básico para limitar requests por IP.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}
        super().__init__(get_response)
    
    def process_request(self, request):
        # Obtener IP del cliente
        ip = self.get_client_ip(request)
        
        # Limitar a 100 requests por minuto por IP
        import time
        current_time = time.time()
        
        if ip in self.requests:
            # Limpiar requests antiguos (más de 1 minuto)
            self.requests[ip] = [
                req_time for req_time in self.requests[ip] 
                if current_time - req_time < 60
            ]
            
            # Verificar límite
            if len(self.requests[ip]) >= 100:
                logger.warning(f"Rate limit exceeded for IP: {ip}")
                return HttpResponse("Rate limit exceeded", status=429)
        else:
            self.requests[ip] = []
        
        # Agregar request actual
        self.requests[ip].append(current_time)
        
        return None
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class LoggingMiddleware(MiddlewareMixin):
    """
    Middleware para logging de seguridad.
    """
    
    def process_request(self, request):
        # Log de requests sospechosos
        if request.method in ['POST', 'PUT', 'DELETE']:
            logger.info(f"Security: {request.method} request to {request.path} from {self.get_client_ip(request)}")
        
        return None
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
