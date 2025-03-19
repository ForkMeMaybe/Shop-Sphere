# from django.contrib import admin
# from .models import Lead


# @admin.register(Lead)
# class LeadAdmin(admin.ModelAdmin):
#     list_display = (
#         "name",
#         "email",
#         "phone",
#         "source",
#         "engagement_level",
#         "score",
#         "created_at",
#     )
#     list_filter = ("source", "engagement_level", "created_at")
#     search_fields = ("name", "email", "phone")
#     ordering = ("-created_at",)
#     readonly_fields = ("created_at", "score")
#     fieldsets = (
#         ("Personal Info", {"fields": ("name", "email", "phone")}),
#         ("Lead Details", {"fields": ("source", "engagement_level", "score")}),
#         ("Timestamps", {"fields": ("created_at",)}),
#     )



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
        "get_products",  # Add this method to display products
    )
    list_filter = ("source", "engagement_level", "created_at")
    search_fields = ("name", "email", "phone")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "score")

    fieldsets = (
        ("Personal Info", {"fields": ("name", "email", "phone")}),
        ("Lead Details", {"fields": ("source", "engagement_level", "score", "products")}),  # Include products here
        ("Timestamps", {"fields": ("created_at",)}),
    )

    def get_products(self, obj):
        """Returns a comma-separated list of product titles for display."""
        return ", ".join([product.title for product in obj.products.all()])

    get_products.short_description = "Products"  # Sets column name in admin panel
