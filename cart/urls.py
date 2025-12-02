from django.urls import path
from .views import CartAddview,CartListview,Deletecartview,CartUpadateview


urlpatterns = [
    path('add/',CartAddview.as_view()),
    path('list/',CartListview.as_view()),
    path('delete/<int:item_id>/',Deletecartview.as_view()),
    path('update/<int:item_id>/',CartUpadateview.as_view()),
]
