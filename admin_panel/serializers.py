from rest_framework import serializers
from accounts.models import Register
from products.models import Product
from products.models import Category

#usermanagement

class AdminUserManageserializer(serializers.ModelSerializer):
    class Meta:
        model=Register
        fields=['id','first_name','email','is_suspend']

#product managemnt session

class Productfetchserializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','name','new_price','descreption','status']


class EditproductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['name','new_price','descreption']


class ProductAddSerializer(serializers.ModelSerializer):
    category=serializers.CharField()

    class Meta:
        model=Product
        fields=['name','descreption','image','category','new_price','status']
    
    def create(self,validated_data):
        category_name=validated_data.pop("category")

        category_obj,Created=Category.objects.get_or_create(name=category_name)

        validated_data["category"]=category_obj

        return Product.objects.create(**validated_data)
    
#ordermanagement

class Orderfetchserializer(serializers.Serializer):
    orderid=serializers.IntegerField()
    user_name=serializers.CharField()
    product_name=serializers.CharField()
    product_price=serializers.IntegerField()
    email=serializers.EmailField()
    order_status=serializers.CharField()
    order_date=serializers.DateTimeField()
    product_quantity = serializers.IntegerField()

class EditOrderSerializer(serializers.Serializer):
    status=serializers.CharField()

    def update(self,instance,validated_data):
        instance.status=validated_data.get('status',instance.status)
        instance.save()
        return instance
