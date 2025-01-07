from .common import *

SECRET_KEY = "django-insecure-#cfv0anz362tub&z7&cs3by87pa1l@7d%@3@bylt23!-+89wfn"

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
