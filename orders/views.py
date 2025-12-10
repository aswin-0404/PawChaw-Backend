from django.shortcuts import render 
from rest_framework.response import Response
from rest_framework import status
from .models import Order,OrderItem
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import CreateOrderSerializer,OrderSerializer
from cart.models import CartItems
import razorpay
from django.conf import settings
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
    
class CreateRazorpayOrder(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        user=request.user

        cart_items=CartItems.objects.filter(user=user)
        total=sum(item.product.new_price*item.quantity for item in cart_items)
        razorpay_amount=int(total*100)

        print("TOTAL:", total)

        client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

        order_data={
            "amount":razorpay_amount,
            "currency":"INR",
            "payment_capture":1,
        }

        razorpay_order=client.order.create(order_data)

        return Response({
            "success":True,
            "order_id":razorpay_order["id"],
            "amount":razorpay_amount,
            "key":settings.RAZORPAY_KEY_ID,
        })

class VerifyRazorpayPayment(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        data=request.data 

        client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id":data["razorpay_order_id"],
                "razorpay_payment_id":data["razorpay_payment_id"],
                "razorpay_signature":data["razorpay_signature"],
            })
        except:
            return Response({"success":False,"message":"Signature verification failed!"},status=status.HTTP_400_BAD_REQUEST)

        serializer=CreateOrderSerializer(data=data["order_data"],context={"request":request})

        if serializer.is_valid():
            order=serializer.save()
            CartItems.objects.filter(user=request.user).delete()
            return Response({"success":True,"order":CreateOrderSerializer(order).data})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)