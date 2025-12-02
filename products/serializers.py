from rest_framework import serializers
from .models import Category,Product

class Productserializer(serializers.ModelSerializer):
    category=serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all()
    )
    class Meta:
        model=Product
        fields=['id','name','descreption','image','category','new_price','status']

