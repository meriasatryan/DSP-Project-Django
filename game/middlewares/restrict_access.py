from django.http import HttpResponseForbidden
import os


class RestrictAccessMiddleware:
    allowed_ips = ["127.0.0.1", os.environ.get("DSP_IP"), os.environ.get("SSP_IP")]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.META['REMOTE_ADDR'] not in self.allowed_ips:
            return HttpResponseForbidden('<h1>Access Forbidden</h1>')

        response = self.get_response(request)
        return response
