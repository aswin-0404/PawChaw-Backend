from rest_framework import serializers
from .models import Order,OrderItem
from products.models import Product

class OrderItemserializer(serializers.ModelSerializer):
    product_name=serializers.CharField(source='product.name',read_only=True)
    product_image=serializers.CharField(source='product.image',read_only=True)

    class Meta:
        model=OrderItem
        fields=['id','product','product_name','product_image','quantity','price']

class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemserializer(many=True,read_only=True)

    class Meta:
        model=Order
        fields=[
            'id',
            'user',
            'full_name',
            'email',
            'address',
            'city',
            'zip',
            'phone',
            'payment_method',
            'status',
            'created_at',
            'items'
        ]

class CreateOrderSerializer(serializers.ModelSerializer):
    items=OrderItemserializer(many=True)

    class Meta:
        model=Order
        fields=[
            'full_name',
            'email',
            'address',
            'city',
            'zip',
            'phone',
            'payment_method',
            'items'
        ]

        def create(self,validated_data):
            items_data=validated_data.pop('items')
            user=self.context['request'].user

            order=Order.objects.create(user=user,**validated_data)

            for items in items_data:
                OrderItem.objects.create(order=order,**items)

            return order