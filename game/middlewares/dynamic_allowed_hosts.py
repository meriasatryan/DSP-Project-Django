from django.conf import settings
import os


class DynamicAllowedHostsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        ip_address = os.environ.get("DSP_IP")
        print("DSP IP:", ip_address)
        if ip_address not in settings.ALLOWED_HOSTS:
            settings.ALLOWED_HOSTS += [ip_address]

    def __call__(self, request):
        response = self.get_response(request)
        return response
