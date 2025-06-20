
# from django.core.mail import send_mail
# from django.conf import settings

# def send_test_email():
#     subject = "Hello from Django"
#     message = "This is a test email sent from Django project."
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = ['receiver@example.com']  # ✅ Change to actual recipient

#     send_mail(subject, message, from_email, recipient_list)




from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(user_email):
    subject = "Welcome to our platform!"
    message = "Thank you for registering."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['luckeykarn0327@gmail.com']
    send_mail(subject, message,from_email,recipient_list, [user_email])
    return "Email sent to " + user_email
