import random
from django.core.mail import send_mail

def generate_otp():
    return f"{random.randint(100000, 999999)}"
def send_verification_email(user):
    otp = generate_otp()
    user.email_otp = otp
    user.save()
    send_mail(
        subject="Verify your email for BD Counselling",
        message=f"Hi {user.name},\nYour verification OTP is: {otp}",
        from_email="noreply@bdcounselling.com",
        recipient_list=[user.email],
    )
