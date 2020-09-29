from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.loginpage, name="login"),
    path('logout/', views.logoutpage, name="logout"),
    path('user/', views.userpage, name="userpage"),
    path('account/', views.accountSetting, name="account"),
    path('products/', views.product, name="product"),
    path('customer/<str:pk>/', views.customer, name="customer"),
    path('create_order/', views.createOrder, name="create_order"),
    path('update_order/<str:pk1>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk2>/', views.deleteOrder, name="delete_order"),
    path('update_customer/<str:pk3>/',
         views.updateCustomer, name="update_customer"),

]
