from rest_framework import serializers
from .models import CartItems
from products.serializers import Productserializer
from products.models import Product

# class Cartserializer(serializers.ModelSerializer):
#     product_id=serializers.IntegerField()
#     product=Productserializer(read_only=True)

#     class Meta:
#         model=CartItems
#         fields=['id','product_id','product','quantity']
        
class Cartserializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    product = Productserializer(read_only=True)

    class Meta:
        model = CartItems
        fields = ['id', 'product_id', 'product', 'quantity']

    def create(self, validated_data):
        product_id = validated_data.pop('product_id')
        user = self.context['request'].user
        product = Product.objects.get(id=product_id)

        return CartItems.objects.create(
            user=user,
            product=product,
            **validated_data
        )
