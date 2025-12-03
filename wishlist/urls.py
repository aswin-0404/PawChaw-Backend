from django.urls import path
from .views import Listwishlist,Removefromwishlistview,Addtowishlistview

urlpatterns = [
    path('list/',Listwishlist.as_view()),
    path('add/',Addtowishlistview.as_view()),
    path('remove/<int:item_id>/',Removefromwishlistview.as_view()),
]
