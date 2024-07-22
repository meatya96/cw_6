from django.core.mail import send_mail
from django.conf import settings
import smtplib
from django.apps import apps


def send_email(subject, message, recipient_list, newsletter):
    SendAttempt = apps.get_model('main', 'SendAttemp')
    try:
        server_response = send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        SendAttempt.objects.create(
            newsletter=newsletter,
            status=SendAttempt.SUCCESS,
            server_response=str(server_response)
        )
    except smtplib.SMTPException as e:
        SendAttempt.objects.create(
            newsletter=newsletter,
            status=SendAttempt.FAILURE,
            server_response=str(e)
        )
