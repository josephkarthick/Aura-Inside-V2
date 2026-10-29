import logging
from datetime import datetime

logger = logging.getLogger("aurainside")

class RequestLogMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        # Skip media & static files
        if request.path.startswith('/media/') or request.path.startswith('/static/'):
            return response

        username = request.user.username if request.user.is_authenticated else "NA"

        ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip:
            ip = ip.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR', 'NA')

        method = request.method
        path = request.get_full_path()
        status = response.status_code
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        logger.info(
            f"{username} | {time} | {ip} | {method} | {path} | {status}"
        )

        return response