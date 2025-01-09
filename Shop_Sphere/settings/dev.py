from .common import *


CELERY_BROKER_URL = "redis://localhost:6379/1"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "shop_sphere",
        "USER": "odd",
        "PASSWORD": "aezakmi",
        "HOST": "localhost",
    }
}


EMAIL_HOST = "localhost"
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_PORT = 2525

if DEBUG:
    MIDDLEWARE += ["silk.middleware.SilkyMiddleware"]

SECRET_KEY = "django-insecure-#cfv0anz362tub&z7&cs3by87pa1l@7d%@3@bylt23!-+89wfn"
