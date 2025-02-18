from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="core/index.html")),
    path("register/", views.register, name="register"),
    path("get_csrf_token/", views.get_csrf_token, name="get_csrf_token"),
    path("verify_otp/", views.verify_otp, name="verify_otp"),
]
