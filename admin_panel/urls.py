from django.urls import path
from .views import AdminDashboard,Adminuserlistview,AdminUsersuspendview,ProductFetchview,ProductDeactivateView,EditProductView,ProductAddView,OrderFetchview,OrderDeleteView

urlpatterns = [
    path('dashboard/',AdminDashboard.as_view()),

    path('userManage/',Adminuserlistview.as_view()),
    path('suspend/<int:id>/',AdminUsersuspendview.as_view()),

    path('products/',ProductFetchview.as_view()),
    path('products/<int:id>/',ProductDeactivateView.as_view()),
    path('products/edit/<int:id>/',EditProductView.as_view()),
    path('products/add/',ProductAddView.as_view()),

    path('order/',OrderFetchview.as_view()),
    path('order/delete/<int:id>/',OrderDeleteView.as_view()),
]
