from .common import *


ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8001",
    "http://localhost:8001",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8001",
    "http://localhost:8001",
    "http://127.0.0.1:8002",
    "http://localhost:8002",
]

# CSRF_COOKIE_HTTPONLY = False  # Allows JavaScript to read the CSRF cookie
# CSRF_USE_SESSIONS = False  # Store CSRF token in a cookie, not session

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

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "shop_sphere_database_meuh",
#         "USER": "shop_sphere_database_meuh_user",
#         "PASSWORD": "3MOZr9BdDEm5AmtBYuHBTzjQS0yy3w4b",
#         "HOST": "dpg-cv7fd0rtq21c73ap9ts0-a.oregon-postgres.render.com",
#     }
# }
DEFAULT_FROM_EMAIL = "beast41514@gmail.com"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "beast41514@gmail.com"
EMAIL_HOST_PASSWORD = "fwee efgl acxw idgs"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

if DEBUG:
    # MIDDLEWARE += ["silk.middleware.SilkyMiddleware"]
    # INSTALLED_APPS += ["debug_toolbar"]
    # MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INTERNAL_IPS = ["127.0.0.1"]

SECRET_KEY = "django-insecure-#cfv0anz362tub&z7&cs3by87pa1l@7d%@3@bylt23!-+89wfn"
