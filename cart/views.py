from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from products.models import Product
from .models import CartItems
from .serializers import Cartserializer

# Create your views here.
class CartListview(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        items=CartItems.objects.filter(user=request.user)
        serializer=Cartserializer(items,many=True)
        return Response(serializer.data)

class CartAddview(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        product_id=request.data.get('product_id')
        quantity=request.data.get('quantity',1)

        try:
            product=Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error":"product not found"},status=status.HTTP_404_NOT_FOUND)
        
        cart_item,created=CartItems.objects.get_or_create(user=request.user,product=product)

        if not created:
            cart_item.quantity +=int(quantity)
            cart_item.save()
        else:
            cart_item.quantity=quantity
            cart_item.save()

        return Response({"message":"succesfully Added to cart!"})
    
class Deletecartview(APIView):
    permission_classes=[IsAuthenticated]

    def delete(self,request,item_id):
        try:
            item=CartItems.objects.get(id=item_id,user=request.user)
        except CartItems.DoesNotExist:
            return Response({"error":"item not found"},status=status.HTTP_404_NOT_FOUND)
        
        if item:
            item .delete()
            return Response({"message":"Item removed Successfully"},status=status.HTTP_200_OK)
        

class CartUpadateview(APIView):
    permission_classes=[IsAuthenticated]
    def patch(self,request,item_id):
        try: 
            item=CartItems.objects.get(id=item_id,user=request.user)
        except CartItems.DoesNotExist:
            return Response({"error":"Not found"},status=status.HTTP_404_NOT_FOUND)
        
        qnty=request.data.get("quantity")
        if qnty is not None:
            item.quantity=qnty
            item.save()
            return Response({"message":"Quantity Updated"})
