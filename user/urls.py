from django.urls import path
from django.http import HttpResponse
from .views import *


urlpatterns = [
    path("", homepage, name="homepage"),
    path("productpage/", productpage, name="productpage"),
    path('aboutus/', aboutus, name='aboutus'),
    path('contactus/', contactus, name='contactus'),
    path("productdetail/<int:product_id>", productdetail, name="productdetail"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("add_to_cart/<int:product_id>", add_to_cart, name="add_to_cart"),
    path("cartlist/", cartlist, name="cartlist"),
    path('order/<int:product_id>/<int:cart_id>',order_item,name='order'),
    path('myorder/',orderlist,name='myorder'),
    # for esewa form
    path('esewaform/', EsewaView.as_view(), name='esewaform'),
    path('esewaverify/<int:order_id>/<int:cart_id>',esewa_verify,name='esewaverify'),
    path('profile/', user_profile, name='profile'),
    
    
]
