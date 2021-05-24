from celery import shared_task
from django.core.mail import EmailMessage

@shared_task
def send_mail(data):
    subject = data['subject']
    body =  data['body']
    email = EmailMessage(subject=subject, body=body, to=[data['to']])
    email.send()