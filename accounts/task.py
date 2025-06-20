from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(user_email):
    import time
    print("send mail is called")
    time.sleep(20)
    print("***********send email called ****************", user_email)
    subject = "Welcome to our platform!"
    message = "Thank you for registering."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email] 

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    return "Email sent to " + user_email


# celery -A mainproject worker -l info --pool=solo