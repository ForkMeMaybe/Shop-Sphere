from django.urls import path
from . import views

urlpatterns = [
    # path("hello/", views.HelloView.as_view())
    path("hello/", views.hello)
]
