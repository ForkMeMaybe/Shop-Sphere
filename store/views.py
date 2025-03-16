from rest_framework.views import APIView
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponseBadRequest
from typing import Any
from django.db.models import Count, Avg
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from requests.sessions import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import PermissionDenied
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
)
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .models import (
    Cart,
    CartItem,
    Collection,
    Customer,
    Order,
    Product,
    OrderItem,
    ProductImage,
    Review,
    Address,
)
from .serializers import (
    AddCartItemSerializer,
    CartItemSerializer,
    CartSerializer,
    CollectionSerializer,
    CreateOrderSerializer,
    CustomerSerializer,
    OrderSerializer,
    ProductImageSerializer,
    ProductSerializer,
    ReviewSerializer,
    UpdateCartItemSerializer,
    UpdateOrderSerializer,
    PaymentSerializer,
    AddressSerializer,
)
from .filters import ProductFilter
from rest_framework.generics import GenericAPIView
from .pagination import DefaultPagination

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET)
)


class PaymentView(GenericAPIView):
    serializer_class = PaymentSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            currency = "INR"
            amount = (
                serializer.validated_data["amount"] * 100
            )  # Razorpay expects amount in paise

            razorpay_order = razorpay_client.order.create(
                dict(amount=amount, currency=currency, payment_capture="0")
            )

            return Response(
                {
                    "razorpay_order_id": razorpay_order["id"],
                    "razorpay_merchant_key": settings.RAZOR_KEY_ID,
                    "razorpay_amount": amount,
                    "currency": currency,
                    "callback_url": "/payments-handler/",
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request):
    #     currency = "INR"
    #     amount = request.data.get("amount")  # Get amount from frontend
    #
    #     if not amount:
    #         return Response({"error": "Amount is required"}, status=400)
    #
    #     razorpay_order = razorpay_client.order.create(
    #         dict(amount=amount, currency=currency, payment_capture="0")
    #     )
    #
    #     razorpay_order_id = razorpay_order["id"]
    #     callback_url = "/paymenthandler/"
    #
    #     return Response(
    #         {
    #             "razorpay_order_id": razorpay_order_id,
    #             "razorpay_merchant_key": settings.RAZOR_KEY_ID,
    #             "razorpay_amount": amount,
    #             "currency": currency,
    #             "callback_url": callback_url,
    #         }
    #     )


# @method_decorator(csrf_exempt, name="dispatch")
# class PaymentHandlerView(APIView):
#     def post(self, request):
#         try:
#             payment_id = request.POST.get("razorpay_payment_id", "")
#             razorpay_order_id = request.POST.get("razorpay_order_id", "")
#             signature = request.POST.get("razorpay_signature", "")
#
#             params_dict = {
#                 "razorpay_order_id": razorpay_order_id,
#                 "razorpay_payment_id": payment_id,
#                 "razorpay_signature": signature,
#             }
#
#             result = razorpay_client.utility.verify_payment_signature(params_dict)
#             if result:
#                 try:
#                     razorpay_client.payment.capture(payment_id, 20000)
#                     return Response({"message": "Payment successful"})
#                 except:
#                     return Response(
#                         {"error": "Error capturing payment"},
#                         status=status.HTTP_400_BAD_REQUEST,
#                     )
#             else:
#                 return Response(
#                     {"error": "Invalid payment signature"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#         except:
#             return HttpResponseBadRequest()


@method_decorator(csrf_exempt, name="dispatch")
class PaymentHandlerView(APIView):
    def post(self, request):
        try:
            # ✅ Use `request.data` instead of `request.POST`
            payment_id = request.data.get("razorpay_payment_id", "")
            razorpay_order_id = request.data.get("razorpay_order_id", "")
            signature = request.data.get("razorpay_signature", "")

            # ✅ Validate required fields
            if not payment_id or not razorpay_order_id or not signature:
                return Response(
                    {"error": "Missing required payment details"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            params_dict = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            }

            # ✅ Verify payment signature
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result:
                try:
                    # 🔥 Fetch the correct amount from the order Razorpay object
                    order = razorpay_client.order.fetch(razorpay_order_id)
                    amount = order["amount"]  # ✅ Use the exact amount from the order

                    # ✅ Capture the payment
                    razorpay_client.payment.capture(payment_id, amount)
                    return Response({"message": "Payment successful"})
                except:
                    return Response(
                        {"error": "Error capturing payment"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"error": "Invalid payment signature"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                {"error": f"Server error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ProductViewSet(ModelViewSet):
    queryset = (
        Product.objects.prefetch_related("images")
        .annotate(review_count=Count("reviews"), average_rating=Avg("reviews__stars"))
        .all()
    )
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ["title", "description"]
    ordering_fields = ["unit_price", "last_update"]

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs["pk"]).count() > 0:
            return Response(
                {
                    "error": "product cannot be deleted because it is associated with an order item"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs["pk"]).count() > 0:
            return Response(
                {
                    "error:": "Collection cannot be deleted because it includes one or more products"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to create a review.")
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Review.objects.filter(
            product_id=self.kwargs["product_pk"]
        ).select_related("user")

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}


class CartViewSet(
    CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet
):
    queryset = Cart.objects.prefetch_related("items__product").all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        return CartItem.objects.prefetch_related("product").filter(
            cart_id=self.kwargs["cart_pk"]
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=["get", "put"], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == "GET":
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class AddressViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Address.objects.all()

        customer_id = Customer.objects.only("id").get(user_id=user.id)
        return Address.objects.filter(customer_id=customer_id)


class OrderViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data, context={"user_id": self.request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()

        customer_id = Customer.objects.only("id").get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrderSerializer
        elif self.request.method == "PATCH":
            return UpdateOrderSerializer
        return OrderSerializer


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        image = self.get_object()
        return HttpResponse(image.image_blob, content_type="image/jpeg")

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs["product_pk"])

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}
