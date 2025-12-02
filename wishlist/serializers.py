from rest_framework import serializers
from products.serializers import Productserializer
from .models import Wishlist

class Wishlistserializer(serializers.ModelSerializer):
    product=Productserializer(read_only=True)
    product_id=serializers.IntegerField(write_only=True)
    
    class Meta:
        model=Wishlist
        fields=['id','product','product_id']