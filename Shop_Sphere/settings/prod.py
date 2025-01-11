from .common import *
import dj_database_url
import os

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")

REDIS_URL = os.environ.get("REDIS_URL")

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

print("prod.py")
print(os.getenv("DJANGO_SETTINGS_MODULE"))
print("DEBUG:", DEBUG)

DATABASES = {"default": dj_database_url.config()}

EMAIL_HOST = "localhost"
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_PORT = 2525

SECRET_KEY = os.environ.get("SECRET_KEY")
