from django.contrib import admin
from django.contrib.admin.options import urlencode
from django.db.models import Count
from django.utils.html import format_html
from django.urls import reverse

from store.forms import ProductImageForm
from . import models


# Register your models here.
class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ["product"]
    extra = 0
    model = models.OrderItem
    min_num = 1
    max_num = 10
    readonly_fields = ["unit_price"]


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ["customer"]
    inlines = [OrderItemInline]
    list_display = ["id", "placed_at", "customer"]
    list_per_page = 10


class InventoryFilter(admin.SimpleListFilter):
    title = "inventory"
    parameter_name = "inventory"

    def lookups(self, request, model_admin):
        return [("<10", "Low")]

    def queryset(self, request, queryset):
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)


# class ProductImageInline(admin.TabularInline):
#     model = models.ProductImage
#     readonly_fields = ["thumbnail"]
#
#     def thumbnail(self, instance):
#         # if instance.image.name != "":
#         #     return format_html(f'<img src="{instance.image.url}" class="thumbnail" />')
#         # return ""
#         """Display image stored as BLOB in the admin panel"""
#         if instance.image_blob:
#             # Convert binary data to Base64
#             import base64
#
#             image_base64 = base64.b64encode(instance.image_blob).decode("utf-8")
#             return format_html(
#                 f'<img src="data:image/jpeg;base64,{image_base64}" class="thumbnail" width="100" height="100"/>'
#             )
#         return "No Image"


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    form = ProductImageForm  # Use custom form to handle image uploads
    extra = 1
    readonly_fields = ["thumbnail"]

    def thumbnail(self, instance):
        """Show a thumbnail preview of the stored image"""
        if instance.image_blob:
            import base64

            image_base64 = base64.b64encode(instance.image_blob).decode("utf-8")
            return format_html(
                f'<img src="data:image/jpeg;base64,{image_base64}" class="thumbnail" width="100" height="100"/>'
            )
        return "No Image"


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ["collection"]
    actions = ["clear_inventory"]
    inlines = [ProductImageInline]
    list_display = ["title", "unit_price", "inventory_status", "collection_title"]
    list_editable = ["unit_price"]
    list_per_page = 10
    list_select_related = ["collection"]
    list_filter = ["collection", "last_update", InventoryFilter]
    ordering = ["title"]
    prepopulated_fields = {"slug": ["title"]}
    search_fields = ["title"]

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "OK"

    @admin.action(description="Clear inventory")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request, f"{updated_count} products were successfullt updated."
        )

    class Media:
        css = {"all": ["store/styles.css"]}


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    autocomplete_fields = ["user"]
    list_display = ["first_name", "last_name", "membership", "orders"]
    list_editable = ["membership"]
    list_per_page = 10
    list_select_related = ["user"]
    ordering = ["user__first_name", "user__last_name"]
    search_fields = ["first_name__istartswith", "last_name__istartswith"]

    @admin.display(ordering="orders_count")
    def orders(self, customer):
        url = (
            reverse("admin:store_order_changelist")
            + "?"
            + urlencode({"customer__id": str(customer.id)})
        )
        return format_html('<a href="{}">{} Orders</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(orders_count=Count("order"))


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "products_count"]
    search_fields = ["title"]

    @admin.display(ordering="products_count")
    def products_count(self, collection):
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"collection_id": str(collection.id)})
        )

        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count("products"))
