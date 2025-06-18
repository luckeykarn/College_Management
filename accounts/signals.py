from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import CustomUser

@receiver(pre_save, sender=CustomUser)
def CustomUser_presave(sender, instance, **kwargs):
    print(instance.username,instance.password,instance.email)

    if instance.pk:
        if instance.password != CustomUser.objects.get(id=instance.pk).password:
            print("password changed successfully")
            instance.password = make_password(instance.password)
        else:
            print("password as it is.")
    else:
        instance.password = make_password(instance.password)
    # print("this pre save function is called before stored in database")