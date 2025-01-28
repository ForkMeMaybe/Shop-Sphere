from django.http import JsonResponse
from .utils import generate_otp, validate_otp
from django.core.mail import BadHeaderError, send_mail
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def register(request):
    if request.method == "POST":
        # email = request.POST.get("email")
        try:
            # Parse the JSON body
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
            send_mail(
                "Email Verification OTP",
                f"Your OTP for email verification is: {email_otp}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
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


@csrf_exempt
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
            return JsonResponse(
                {"success": True, "message": "OTP verified successfully."}
            )
        else:
            return JsonResponse({"success": False, "message": "Invalid OTP."})

    return JsonResponse({"success": False, "message": "Invalid request method."})
