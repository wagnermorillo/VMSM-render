import logging

logger = logging.getLogger('django.request')

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Obtener información del visitante
        user_ip = request.META['REMOTE_ADDR']
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        path = request.path

        # Registrar la información
        logger.info(f"IP: {user_ip}, User Agent: {user_agent}, Path: {path}")

        response = self.get_response(request)
        return response
