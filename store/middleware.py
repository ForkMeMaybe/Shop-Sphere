from django.utils.deprecation import MiddlewareMixin
from http import cookies
from django.conf import settings
from django.http import HttpRequest, HttpResponseBase

# Enable support for the "Partitioned" attribute
cookies.Morsel._flags.add("partitioned")
cookies.Morsel._reserved.setdefault("partitioned", "Partitioned")


class CookiePartitioningMiddleware(MiddlewareMixin):
    def process_response(
        self, request: HttpRequest, response: HttpResponseBase
    ) -> HttpResponseBase:
        for name in (
            getattr(settings, f"{prefix}_COOKIE_NAME")
            for prefix in ("CSRF", "SESSION", "LANGUAGE")
            if getattr(settings, f"{prefix}_COOKIE_SECURE", False)  # Ensure it's set
        ):
            if cookie := response.cookies.get(name):
                cookie["Partitioned"] = True  # Mark it as Partitioned

        return response
