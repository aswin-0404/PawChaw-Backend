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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = Cartserializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    def patch(self, request, item_id):
        try:
            item = CartItems.objects.get(id=item_id, user=request.user)
        except CartItems.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        quantity = request.data.get("quantity")
        if quantity is not None:
            item.quantity = quantity
            item.save()
            return Response({"message": "Quantity Updated"})

        return Response({"error": "Quantity is required"}, status=status.HTTP_400_BAD_REQUEST)

