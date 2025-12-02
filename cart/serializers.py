from rest_framework import serializers
from .models import CartItems
from products.serializers import Productserializer

class Cartserializer(serializers.ModelSerializer):
    product_id=serializers.IntegerField(write_only=True)
    product=Productserializer(read_only=True)
    
    class Meta:
        model=CartItems
        fields=['id','product_id','product','quantity']
        