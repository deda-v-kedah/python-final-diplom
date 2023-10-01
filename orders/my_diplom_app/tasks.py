from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from celery import shared_task




@shared_task()
def send(subject, message, recipients):
    from_email=settings.EMAIL_HOST_USER
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, recipients)
        except BadHeaderError:
            print('Invalid header found.')
        print('email sent')
    else:
        print('Make sure all fields are entered and valid.')
