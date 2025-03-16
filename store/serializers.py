from rest_framework import serializers
from django.db import transaction
from decimal import Decimal
from .models import (
    CartItem,
    Collection,
    Customer,
    Order,
    OrderItem,
    Product,
    ProductImage,
    Review,
    Cart,
    Address,
)
from .signals import order_created


class PaymentSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title", "products_count"]

    products_count = serializers.IntegerField(read_only=True)


class ProductImageSerializer(serializers.ModelSerializer):
    image_file = serializers.ImageField(write_only=True)  # Accept file uploads
    image_data = serializers.SerializerMethodField()  # Return Base64 data

    class Meta:
        model = ProductImage
        fields = ["id", "image_file", "image_data"]

    def create(self, validated_data):
        """Handle image upload and store it as BLOB"""
        image_file = validated_data.pop("image_file")
        validated_data["image_blob"] = image_file.read()  # Convert image to binary
        return super().create(validated_data)

    def get_image_data(self, obj):
        """Convert binary image data to Base64 string"""
        if obj.image_blob:
            import base64

            return f"data:image/jpeg;base64,{base64.b64encode(obj.image_blob).decode('utf-8')}"
        return None


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "slug",
            "inventory",
            "unit_price",
            "price_with_tax",
            "collection_id",  # _id because without it a query is being sent to the database to fetch collections
            "images",
            "review_count",
            "average_rating",
        ]

    review_count = serializers.IntegerField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    def calculate_tax(self, product):
        return product.unit_price * Decimal(1.1)


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "user", "description", "date", "stars"]
        read_only_fields = ["user", "id"]

    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id=product_id, **validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "title", "unit_price", "images"]


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]

    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item):
        return cart_item.quantity * cart_item.product.unit_price


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id", "items", "total_price"]

    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum(
            [item.quantity * item.product.unit_price for item in cart.items.all()]
        )


class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "product_id", "quantity"]

    product_id = serializers.IntegerField()

    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data
            )

        return self.instance

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No product with the given id was found.")
        return value


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "phone", "birth_date", "membership"]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "street",
            "city",
            "state",
            "country",
            "postal_code",
            "address_type",
            "is_default",
            "customer",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "unit_price", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "placed_at", "payment_status", "items"]


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["payment_status"]


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    payment_status = serializers.ChoiceField(
        choices=Order.PAYMENT_STATUS_CHOICES, default=Order.PAYMENT_STATUS_PENDING
    )

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError("No cart with the given id was found")
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError("The cart is empty")
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data["cart_id"]
            customer = Customer.objects.get(user_id=self.context["user_id"])
            payment_status = self.validated_data.get(
                "payment_status", Order.PAYMENT_STATUS_PENDING
            )
            order = Order.objects.create(
                customer=customer, payment_status=payment_status
            )

            cart_items = CartItem.objects.select_related("product").filter(
                cart_id=cart_id
            )

            order_items = []
            for item in cart_items:
                # ✅ Reduce product inventory
                item.product.inventory -= item.quantity
                if item.product.inventory < 0:
                    raise serializers.ValidationError(
                        f"Not enough inventory for {item.product.title}"
                    )
                item.product.save()

                order_items.append(
                    OrderItem(
                        order=order,
                        product=item.product,
                        unit_price=item.product.unit_price,
                        quantity=item.quantity,
                    )
                )

            # order_items = [
            #     OrderItem(
            #         order=order,
            #         product=item.product,
            #         unit_price=item.product.unit_price,
            #         quantity=item.quantity,
            #     )
            #     for item in cart_items
            # ]

            OrderItem.objects.bulk_create(order_items)
            Cart.objects.filter(pk=cart_id).delete()

            order_created.send_robust(self.__class__, order=order)

            return order
