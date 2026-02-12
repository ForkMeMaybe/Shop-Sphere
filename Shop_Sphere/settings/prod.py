from .common import *
import dj_database_url
import os
import corsheaders.defaults

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "your_default_agent_api_key")
AWS_SECRET_ACCESS_KEY = os.environ.get(
    "AWS_SECRET_ACCESS_KEY", "your_default_agent_api_key"
)
AWS_DEFAULT_REGION = "us-east-1"


ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")

ANYMAIL = {
    "RESEND_API_KEY" : os.environ.get("RESEND_API_KEY")
}

REDIS_URL = os.environ.get("REDIS_URL")

RAZOR_KEY_ID = os.environ.get("RAZOR_KEY_ID")
RAZOR_KEY_SECRET = os.environ.get("RAZOR_KEY_SECRET")

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8001",
    "http://127.0.0.1:5173",
    "http://localhost:8001",
    "http://localhost:5173",
    "https://shop-sphere-frontend.onrender.com",
]
CSRF_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SECURE = True
CSRF_USE_SESSIONS = False

CORS_ALLOW_HEADERS = [
    *corsheaders.defaults.default_headers,
    "X-Cart-ID",
]

CORS_EXPOSE_HEADERS = [
    "Content-Type",
    "X-CSRFToken",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8001",
    "http://127.0.0.1:5173",
    "http://localhost:8001",
    "http://localhost:5173",
    "https://shop-sphere-frontend.onrender.com",
]

CELERY_BROKER_URL = REDIS_URL

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

DEBUG = os.getenv("DEBUG", "False") == "True"

DATABASES = {"default": dj_database_url.config()}

DEFAULT_FROM_EMAIL = os.environ.get("D EFAULT_FROM_EMAIL")

EMAIL_BACKEND = "anymail.backends.resend.EmailBackend"
# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

SENDGRID_SANDBOX_MODE_IN_DEBUG = False
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

SECRET_KEY = os.environ.get("SECRET_KEY")

SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = True
