from django.core.mail import send_mail
from django.conf import settings

def send_welcome_email(user):
    subject = "Welcome to MySite 🎉"
    message = f"""
Hi {user.username},

Your account has been created successfully.

You can now log in using your email and password.

Regards,
MySite Team
"""
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )