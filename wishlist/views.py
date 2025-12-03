from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import Wishlistserializer
from .models import Wishlist
from rest_framework.response import Response
from rest_framework import status
from products.models import Product


# Create your views here.
class Listwishlist(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        item=Wishlist.objects.filter(user=request.user)
        serializer=Wishlistserializer(item,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class Addtowishlistview(APIView):

    permission_classes=[IsAuthenticated]

    def post(self,request):
        product_id=request.data.get('product_id')

        try:
            product=Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error":"Product not found!"},status=status.HTTP_404_NOT_FOUND)
        
        wish,created=Wishlist.objects.get_or_create(user=request.user,product=product)

        if not created:
            return Response({"message":"Product already in wishlist!"},status=status.HTTP_200_OK)
        return Response({"message":"Product added to wishlist!"})

class Removefromwishlistview(APIView):
    permission_classes=[IsAuthenticated]

    def delete(self,request,item_id):
        try:
            item=Wishlist.objects.get(id=item_id,user=request.user)
            item.delete()
            return Response({"message":"Product removed succesfully"},status=status.HTTP_200_OK)
            
        except Wishlist.DoesNotExist:
            return Response({"error":"Product not in wishlist"},status=status.HTTP_400_BAD_REQUEST)