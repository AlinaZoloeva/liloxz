from django.contrib import admin
from django.urls import path, include

from shopclothes.views import *

urlpatterns = [
    path('', index, name='home'),
    path('shop/<slug:shop_slug>/', shop_cat, name='shop'),
    path('shop/', shop, name='shop'),
    path('detail/<slug:det_slug>/', detail, name='detail'),
    path('contact/', contact, name='contact'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
]