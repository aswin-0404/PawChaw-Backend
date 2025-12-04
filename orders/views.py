from django.shortcuts import render 
from rest_framework.response import Response
from rest_framework import status
from .models import Order,OrderItem
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import CreateOrderSerializer,OrderSerializer
# Create your views here.

class Placeorderview(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        serializer=CreateOrderSerializer(data=request.data,context={"request":request})

        if serializer.is_valid():
            order=serializer.save()
            return Response({
                "message":"orderplaced Succesfully",
                "order":CreateOrderSerializer(order).data
                             },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserOrderview(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        order=Order.objects.filter(user=request.user).order_by('-created_at')
        serializer=OrderSerializer(order,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)