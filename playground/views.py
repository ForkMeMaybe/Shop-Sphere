from django.shortcuts import render
import logging
from rest_framework.views import APIView
import requests
from lead.tasks import process_leads_for_marketing

logger = logging.getLogger(__name__)

#
# class HelloView(APIView):
#     def get(self, request):
#         try:
#             logger.info("Calling httpbin")
#             response = requests.get("https://httpbin.org/delay/2")
#             logger.info("Received the response")
#             data = response.json()
#         except requests.ConnectionError:
#             logger.critical("httpbin is offline")
#         return render(request, "hello.html", {"name": data})


def hello(request):
    process_leads_for_marketing.delay()
    return render(request, "hello.html", {"name": "mosh"})
