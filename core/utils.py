import pyotp


def generate_otp():
    totp = pyotp.TOTP(pyotp.random_base32(), interval=300)  # 5 minutes validity
    return totp.now()


def validate_otp(otp, user_otp):
    return otp == user_otp
