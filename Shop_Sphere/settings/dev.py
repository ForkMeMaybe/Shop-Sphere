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

if DEBUG:
    MIDDLEWARE += ["silk.middleware.SilkyMiddleware"]
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INTERNAL_IPS = ["127.0.0.1"]

SECRET_KEY = "django-insecure-#cfv0anz362tub&z7&cs3by87pa1l@7d%@3@bylt23!-+89wfn"
