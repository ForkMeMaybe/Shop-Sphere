from django.http import HttpResponse
from store.models import Product
from django.shortcuts import render


# Create your views here.
def say_hello(request):
    query_set = Product.objects.filter(unit_price__range=(20, 30))

    return render(
        request, "hello.html", {"name": "Piyush", "products": list(query_set)}
    )
