from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import Registerserializer,Loginserializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
class Registerview(APIView):
    def post(self,request):
        serializer=Registerserializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Registered Successfully!"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
    
class Loginview(APIView):
    def post(self,request):
        serializer=Loginserializer(data=request.data)

        if serializer.is_valid():
            email=serializer.validated_data['email']
            password=serializer.validated_data['password']

            user=authenticate(username=email,password=password)

            if not user:
                return Response({"message":"invalid Credentials!"},status=status.HTTP_404_NOT_FOUND)
            
            if user.is_suspend:
                return Response({"message":"Your accout got suspended!"},status=status.HTTP_403_FORBIDDEN)

            refresh=RefreshToken.for_user(user)
            access=refresh.access_token

            return Response({
                "message":"Login Successfull!",
                "token":{
                    "refresh":str(refresh),
                    "access":str(access)
                },
                "user":{
                    "id":user.id,
                    "first_name":user.first_name,
                    "last_name":user.last_name,
                    "email":user.email,
                    "phone":user.phone,
                    "role":user.role,
                    "is_superuser":user.is_superuser
                    }},status=status.HTTP_200_OK)
            
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            

