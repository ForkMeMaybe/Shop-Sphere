from .common import *
import dj_database_url
import os

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")

DEBUG = os.environ["DEBUG"]

DATABASES = {"default": dj_database_url.config()}

SECRET_KEY = os.environ.get("SECRET_KEY")
