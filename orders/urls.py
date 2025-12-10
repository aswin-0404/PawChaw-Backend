from django.urls import path
from .views import Placeorderview,UserOrderview,CreateRazorpayOrder,VerifyRazorpayPayment

urlpatterns = [
    path('placeorder/',Placeorderview.as_view()),
    path('orderlist/',UserOrderview.as_view()),
    path("create-razorpay-order/",CreateRazorpayOrder.as_view()),
    path("verify-payment/",VerifyRazorpayPayment.as_view()),
]
