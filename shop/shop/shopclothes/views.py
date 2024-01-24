from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from shopclothes.models import *


def index(request):
    products = Product.objects.filter(count_purch__gt=10)
    categ = Category.objects.all()
    obj = {'products': products,
           'categ': categ}
    return render(request, 'index.html', context=obj)

def shop(request):
    products = Product.objects.all()
    categ = Category.objects.all()
    obj = {'products': products,
           'categ': categ,
           }
    return render(request, 'shop.html', context=obj)

def shop_cat(request, shop_slug):
    category = get_object_or_404(Category, slug=shop_slug)
    products = Product.objects.filter(cat__slug=shop_slug)
    categ = Category.objects.all()

    obj = {'products': products,
           'categ': categ,
           'cat_selected': category.pk}
    return render(request, 'shop_cat.html', context=obj)

def detail(request, det_slug):
    product = get_object_or_404(Product, slug=det_slug)
    products = Product.objects.exclude(slug=det_slug)
    categ = Category.objects.all()
    obj = {'product': product,
           'categ': categ,
           'products': products}

    return render(request, 'detail.html', context=obj)

def contact(request):
    return render(request, 'contact.html')

def checkout(request):
    return render(request, 'checkout.html')

def cart(request):
    return render(request, 'cart.html')