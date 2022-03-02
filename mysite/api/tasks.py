from time import sleep
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task


@shared_task
def add_cel(n):
    sleep(n)
    print('hellooooooooo')


@shared_task
def send_mail_after_order(email):
    subject = 'Thank you for the order'
    message = 'Text message'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list)
