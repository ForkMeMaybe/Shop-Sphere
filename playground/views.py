from django.http import HttpResponse
from django.shortcuts import render
from store.models import Product
from tags.models import TaggedItem


# Create your views here.
def say_hello(request):
    queryset = TaggedItem.objects.get_tags_for(Product, 1)

    return render(request, "hello.html", {"name": "Piyush", "tags": list(queryset)})
