from django.shortcuts import render
from django.http import HttpResponse
from .models import Blog
from .models import CustomUser
import random
from faker import Faker

def random_blog(request):
    fake = Faker()
    user_ids = CustomUser.objects.values_list('id', flat=True)

    for num in range(1, 100):
        title = fake.sentence(nb_words=3).rstrip(".")  
        tags = ",".join(fake.words(nb=3))  
        random_user_id = random.choice(user_ids)


        Blog.objects.create(title=title,  user_id=random_user_id, tags=tags)

    return HttpResponse("100 fake blogs created successfully!")
