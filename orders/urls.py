from django.urls import path
from .views import Placeorderview,UserOrderview

urlpatterns = [
    path('placeorder/',Placeorderview.as_view()),
    path('orderlist/',UserOrderview.as_view()),
]
