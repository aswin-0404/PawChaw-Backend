from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order,OrderItem
from accounts.models import Register
from rest_framework.views import APIView
from django.db.models import Count,Sum
from .serializers import AdminUserManageserializer,Productfetchserializer,EditproductSerializer,ProductAddSerializer,Orderfetchserializer
from rest_framework.permissions import IsAdminUser
from django.db.models.functions import TruncMonth
from products.models import Product
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter,OrderingFilter
from django.db.models import F

# Create your views here.

#dashboard section

class AdminDashboard(APIView):
    permission_classes=[IsAdminUser]
    def get(self,request):
        user_count=Register.objects.aggregate(count=Count('id'))
        order_count=Order.objects.aggregate(count=Count('id'))
        earnings=OrderItem.objects.aggregate(sum=Sum('price'))

        monthly_order=(
            Order.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
        )

        return Response({
            'user_count':user_count,
            'order_count':order_count,
            'earnings':earnings,
            'monthly_order':monthly_order,
        },status=status.HTTP_200_OK)
    

#userManagement

class Adminuserlistview(ListAPIView):
    permission_classes=[IsAdminUser]

    def get(self,request):
        users=Register.objects.filter(is_staff=False)
        serializer=AdminUserManageserializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class AdminUsersuspendview(APIView):
    permission_classes=[IsAdminUser]

    def patch(self,request,id):
        try:
           user=Register.objects.get(id=id)

        except Register.DoesNotExist:
            return Response({"Message":"User Not Found"},status=status.HTTP_404_NOT_FOUND)
        
        user.is_suspend=not user.is_suspend
        user.save() 

        serializer=AdminUserManageserializer(user)

        return Response(serializer.data,status=status.HTTP_200_OK)

#Product Management

class ProductFetchview(ListAPIView):
    permission_classes=[IsAdminUser]
    filter_backends=[SearchFilter,OrderingFilter]
    serializer_class=Productfetchserializer
    queryset=Product.objects.all()
    search_fields=['name','category']
    ordering__fields=['id']

    

    # def get(self,request):
    #     product=Product.objects.all()
    #     serializer=Productfetchserializer(product,many=True)
    #     return Response(serializer.data,status=status.HTTP_200_OK)
    
class ProductDeactivateView(APIView):
    permission_classes=[IsAdminUser]

    def patch(self,request,id):
        try:
            product=Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response({"Message":"Product not found"},status=status.HTTP_404_NOT_FOUND)
        
        if product.status=="Active":
            product.status="Inactive"
        else:
            product.status="Active"

        product.save()

        
        serializer=Productfetchserializer(product)
        return Response(serializer.data,status=status.HTTP_200_OK)



class EditProductView(APIView):
    permission_classes=[IsAdminUser]

    def patch(self,request,id):
        try:
            product=Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response({"message":"product not found"},status=status.HTTP_404_NOT_FOUND)
        
        if product:
            serializer=EditproductSerializer(product,data=request.data,partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class ProductAddView(APIView):
    permission_classes=[IsAdminUser]

    def post(self,request):
        serializer=ProductAddSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Product added Succesfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
#ordermanagement

class OrderFetchview(ListAPIView):
    permission_classes=[IsAdminUser]
    serializer_class=Orderfetchserializer
    filter_backends=[SearchFilter,OrderingFilter]

    search_fields=['username','email']
    ordering_fields=['order_date']
    ordering=['-order_date']

    queryset=OrderItem.objects.select_related("order","product").values(
        orderid=F("order__id"),
        user_name=F("order__full_name"),
        product_name=F("product__name"),
        product_price=F("price"),
        product_quantity=F("quantity"),
        email=F("order__email"),
        order_status=F("order__status"),
        order_date=F("order__created_at")
    )

class OrderDeleteView(APIView):
    permission_classes=[IsAdminUser]

    def delete(self,request,id):
        try:
            order=Order.objects.get(id=id)
            order.delete()
        except Order.DoesNotExist:
            return Response({"message":"order not found"},status=status.HTTP_400_BAD_REQUEST)

    
