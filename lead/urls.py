from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeadViewSet

router = DefaultRouter()
router.register("leads", LeadViewSet)

urlpatterns = (router.urls)
