from django.db import models
from store.models import Product


# Create your models here.
class Lead(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    source = models.CharField(
        max_length=100,
        choices=[
            ("website", "Website"),
        ],
    )
    engagement_level = models.IntegerField(
        choices=[(0, "Visit"), (1, "Search"), (2, "Add to Cart"), (3, "Payment Page")]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(default=0.0)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.name
