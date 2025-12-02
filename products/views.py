from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListAPIView,RetrieveAPIView
from .serializers import Productserializer
from .models import Product

# Create your views here.
class productsview(ListAPIView):
    serializer_class=Productserializer

    def get_queryset(self):
        queryset=Product.objects.all()
        categorie=self.request.query_params.get('category')

        if categorie:
           queryset=queryset.filter(category__name__iexact=categorie)
        else:
            queryset=Product.objects.filter(status='Active')
        return queryset

class Productdetailview(RetrieveAPIView):
    queryset=Product.objects.all()
    serializer_class=Productserializer
    lookup_field='id'