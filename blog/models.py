from django.db import models
from accounts.models import CustomUser
# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length = 4000)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="myblogs")
    tags =  models.CharField(max_length = 4000)

    def __str__(self):
        return self.title