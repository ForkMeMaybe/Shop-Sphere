from django.http import JsonResponse, HttpResponse
from requests import Response
from .utils import generate_otp, validate_otp
from django.core.mail import BadHeaderError
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
import json
from templated_mail.mail import BaseEmailMessage
from smtplib import SMTPException
from django.shortcuts import render
from django.middleware.csrf import get_token
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.middleware.csrf import get_token


@ensure_csrf_cookie
@require_http_methods(["GET"])
def get_csrf_token(request):
    response = JsonResponse(
        {"message": "Placed csrf cookie in response head and cookie"}, status=200
    )
    response["X-CSRFToken"] = request.META.get("CSRF_COOKIE", "")
    return response


# @ensure_csrf_cookie
def register(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON format."})

        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({"success": False, "message": "Invalid email format."})

        email_otp = generate_otp()
        redis_key = f"otp:{email}"
        cache.set(redis_key, email_otp)

        try:
            message = BaseEmailMessage(
                template_name="emails/otp_template.html",
                context={"email_otp": email_otp},
            )
            message.send([email])
        except (BadHeaderError, SMTPException) as e:
            return JsonResponse(
                {"success": False, "message": f"Failed to send OTP. Error: {str(e)}"}
            )

        return JsonResponse(
            {
                "success": True,
                "message": "OTP sent successfully. Please check your email.",
            }
        )
    #     csrf_token = get_token(request)
    #
    #     response = JsonResponse({"message": "CSRF token set."})
    #
    #     response["Set-Cookie"] = (
    #         f"csrftoken={csrf_token}; Path=/; Secure; HttpOnly; SameSite=None; Partitioned"
    #     )
    #
    #     return response


def verify_otp(request):
    if request.method == "POST":
        # email = request.POST.get("email")
        # user_otp = request.POST.get("otp")
        try:
            # Parse the JSON body
            data = json.loads(request.body)
            email = data.get("email")
            user_otp = data.get("otp")
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON format."})

        if not email or not user_otp:
            return JsonResponse(
                {"success": False, "message": "Email and OTP are required."}
            )

        redis_key = f"otp:{email}"
        stored_otp = cache.get(redis_key)

        if stored_otp is None:
            return JsonResponse(
                {"success": False, "message": "OTP expired or not found."}
            )

        if validate_otp(stored_otp, user_otp):
            cache.delete(redis_key)
            return JsonResponse(
                {"success": True, "message": "OTP verified successfully."}
            )
        else:
            return JsonResponse({"success": False, "message": "Invalid OTP."})

    return JsonResponse({"success": False, "message": "Invalid request method."})
