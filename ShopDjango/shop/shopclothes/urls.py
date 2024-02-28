from django.contrib import admin
from django.urls import path, include

from shopclothes.views import *

urlpatterns = [
    path('', index, name='home'),
    path('shop/<slug:shop_slug>/', shop_cat, name='shop'),
    path('shop/', shop, name='shop'),
    path('detail/<slug:det_slug>/', detail, name='detail'),
    path('cart-add/<slug:add_slug>/', add_cart, name='addcart'),
    path('cart-delete/<slug:slug>/', cart_delete, name='deletecart'),
    path('contact/', contact, name='contact'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
]