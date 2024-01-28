from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView

from shopclothes.forms import RegisterUserForm, LoginUserForm
from shopclothes.models import *
from shopclothes.utils import DataMixin


def index(request):
    products = Product.objects.filter(count_purch__gt=10)
    categ = Category.objects.all()
    gender = Gender.objects.all()
    try:
        cart = Cart.objects.filter(user=request.user)
    except:
        cart = []
        obj = {'products': products,
               'categ': categ,
               'gender': gender,
               'cart_count': 0,
               'cat_selected': 1}
        return render(request, 'index.html', context=obj)

    obj = {'products': products,
           'categ': categ,
           'gender': gender,
           'cart_count': cart.count(),
           'cat_selected': 1}
    return render(request, 'index.html', context=obj)

def shop(request):
    products = Product.objects.all()
    categ = Category.objects.all()

    try:
        cart = Cart.objects.filter(user=request.user)
    except:
        cart = []
        obj = {'products': products,
               'categ': categ,
               'cart_count': 0,
               'cat_selected': 2,
               }
        return render(request, 'shop.html', context=obj)

    obj = {'products': products,
           'categ': categ,
           'cart_count': cart.count(),
           'cat_selected': 2,
           }
    return render(request, 'shop.html', context=obj)



def shop_cat(request, shop_slug):
    if shop_slug in ('women', 'man', 'child'):
        products = Product.objects.filter(gender__slug=shop_slug)
    else:
        products = Product.objects.filter(cat__slug=shop_slug)
    categ = Category.objects.all()

    try:
        cart = Cart.objects.filter(user=request.user)
    except:
        cart = []
        obj = {'products': products,
               'categ': categ,
               'cart_count': 0,
               'cat_selected:': 2,
               }
        return render(request, 'shop_cat.html', context=obj)

    obj = {'products': products,
           'categ': categ,
           'cart_count': cart.count(),
           'cat_selected': 2,
           }
    return render(request, 'shop_cat.html', context=obj)

def detail(request, det_slug):
    product = get_object_or_404(Product, slug=det_slug)
    products = Product.objects.exclude(slug=det_slug)
    categ = Category.objects.all()

    try:
        cart = Cart.objects.filter(user=request.user)
    except:
        cart=[]
        obj = {'categ': categ,
               'product': product,
               'products': products,
               'cart_count': 0}
        return render(request, 'detail.html', context=obj)

    obj = {'product': product,
           'categ': categ,
           'products': products,
           'cart_count': cart.count()}

    return render(request, 'detail.html', context=obj)

def contact(request):
    categ = Category.objects.all()
    try:
        cart = Cart.objects.filter(user=request.user)
    except:
        cart=[]
        obj = {'categ': categ,
               'cart_count': 0,
               'cat_selected': 3}
        return render(request, 'contact.html', context=obj)
    obj = {'categ': categ,
           'cart_count': cart.count(),
           'cat_selected': 3}
    return render(request, 'contact.html', context=obj)

def checkout(request):
    categ = Category.objects.all()
    try:
        cart = Cart.objects.filter(user=request.user)
    except:
        cart=[]
        obj = {'categ': categ,
               'cart_count': 0,
               'total': 0,
               'subtotal': 0}
        return render(request, 'checkout.html', context=obj)

    subtotal = 0

    for i in cart:
        subtotal += (i.product.price * i.count)
    total = subtotal + 10

    obj = {'categ': categ,
           'cart': cart,
           'cart_count': cart.count(),
           'total': total,
           'subtotal': subtotal}
    return render(request, 'checkout.html', context=obj)

def cart(request):
    products = Product.objects.filter(count_purch__gt=10)
    categ = Category.objects.all()
    try:
        cart = Cart.objects.filter(user=request.user)
    except:
        cart=[]
        obj = {'products': products,
               'categ': categ,
               'cart': cart,
               'cart_count': 0}
        return render(request, 'cart.html', context=obj)

    subtotal = 0

    for i in cart:
        subtotal += (i.product.price * i.count)
    total = subtotal + 10


    obj = {'products': products,
           'categ': categ,
           'cart': cart,
           'cart_count': cart.count(),
           'total': total,
           'subtotal': subtotal}

    return render(request, 'cart.html', context=obj)

def add_cart(request, add_slug):
    product = Product.objects.get(slug=add_slug)

    carts = Cart.objects.filter(user=request.user, product=product)

    if not carts.exists():
        cart = Cart(user=request.user, product=product, count=1)
        cart.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        cart = carts.first()
        cart.count += 1
        cart.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def cart_delete(request, slug):
    carts = Cart.objects.filter(user=request.user, product__slug=slug)
    cart = carts.first()
    if cart.count > 1:
        cart = carts.first()
        cart.count -= 1
        cart.save()
    elif cart.count == 1:
        cart = carts.first()
        cart.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('home')

