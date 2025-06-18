from rest_framework import serializers
from ..models import Blog
from accounts.serializers.customuser_serializers import XotusaCustomUserListSerializers

class BlogListSerializers(serializers.ModelSerializer):
    user = XotusaCustomUserListSerializers()
    class Meta:
        model = Blog
        fields = ['id','title','user','tags']

class BlogRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

class BlogWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'