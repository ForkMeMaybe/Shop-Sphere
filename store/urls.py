from django.urls import path
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("products", views.ProductViewSet)
router.register("collections", views.CollectionViewSet)
router.register("carts", views.CartViewSet)
router.register("customers", views.CustomerViewSet)
router.register("orders", views.OrderViewSet, basename="orders")

products_router = routers.NestedDefaultRouter(router, "products", lookup="product")
products_router.register("reviews", views.ReviewViewSet, basename="product-reviews")
products_router.register("images", views.ProductImageViewSet, basename="product-images")

carts_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
carts_router.register("items", views.CartItemViewSet, basename="cart-items")

customer_router = routers.NestedDefaultRouter(router, "customers", lookup="customer")
customer_router.register(
    "addresses", views.AddressViewSet, basename="customer-addresses"
)

urlpatterns = (
    router.urls
    + products_router.urls
    + carts_router.urls
    + customer_router.urls
    + [path("payments/", views.PaymentView.as_view(), name="payment")]
    + [
        path(
            "payments-handler/",
            views.PaymentHandlerView.as_view(),
            name="payment-handler",
        )
    ]
)
