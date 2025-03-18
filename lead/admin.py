from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone",
        "source",
        "engagement_level",
        "score",
        "created_at",
    )
    list_filter = ("source", "engagement_level", "created_at")
    search_fields = ("name", "email", "phone")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "score")
    fieldsets = (
        ("Personal Info", {"fields": ("name", "email", "phone")}),
        ("Lead Details", {"fields": ("source", "engagement_level", "score")}),
        ("Timestamps", {"fields": ("created_at",)}),
    )
