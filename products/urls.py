from django.urls import path
from .views import productsview,Productdetailview

urlpatterns = [
    path('list/',productsview.as_view()),
    path('list/<int:id>/',Productdetailview.as_view()),
]
