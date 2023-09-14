from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import AddPostForms, RegisterUserForm, LoginUserForm, ContactForm
from .utils import *


class WomenHome(DataMixin, ListView):
    # ListView автоматически передает в шаблон ссылку на класс пагинатор (paginator) и список объектов для текущей страницы (page_obj)
    # page_range сколько всего страниц
    model = Women # создает коллекцию записей objects list
    template_name = 'women/index.html'
    context_object_name = 'posts' # вместо objects list контекст
    #extra_context = {'title': 'Главная страница'} # Для статических переменных

    def get_context_data(self, *, object_list=None, **kwargs): # Динамический контекст для передачи динамического массива
        context = super().get_context_data(**kwargs) # берем существующий контекст
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items())) # Объединение в общий контекст двух словарей (две верхние строчки)

    def get_queryset(self): # возвращает то, что должно быть прочитано из модели women на первой строке класса
        return Women.objects.filter(is_published=True).select_related('cat')

'''
def index(request):
    context = {
        'fil': None,
        'menu': menu,
        'title': 'Главная страница',
        'cat_selected': 0,
    }

    return render(request, 'women/index.html', context=context)
'''
def about(request):
    cats = Category.objects.all()

    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.pop(1)

    return render(request, 'women/about.html', {'menu': user_menu, 'title': 'О сайте', 'cats': cats})


def categ(request, catid):
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>{catid}</p>")

def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>страница не найдена</h1>")

'''
def addpage(request):
     if request.method == 'POST':
         form = AddPostForms(request.POST, request.FILES)
         if form.is_valid():
             form.save()
             return redirect('home')

     else:
         form = AddPostForms()
     return render(request, 'women/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})
'''
class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForms
    template_name = 'women/addpage.html'
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs): # Динамический контекст для передачи динамического массива
        context = super().get_context_data(**kwargs)  # берем существующий контекст
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')


    def get_context_data(self, *, object_list=None, **kwargs):  # Динамический контекст для передачи динамического массива
        context = super().get_context_data(**kwargs)  # берем существующий контекст
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')

'''
def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)

    context = {
        'post': post,
        'menu': menu,
        'title': post.title,
        'cat_selected': post.cat_id,
    }

    return render(request, 'women/post.html', context=context)

'''

class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    context_object_name = 'post'

    slug_url_kwarg = 'post_slug'
    #pk_url_kwarg = 'post_pk'

    def get_context_data(self, *, object_list=None, **kwargs): # Динамический контекст для передачи динамического массива
        context = super().get_context_data(**kwargs)  # берем существующий контекст
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))

'''
def show_cat(request, cat_slug):
    context = {
        'fil': cat_slug,
        'menu': menu,
        'title': 'Отображение по рубрикам',
        'cat_selected': cat_slug,
    }

    return render(request, 'women/index.html', context=context)
'''

class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs): # Динамический контекст для передачи динамического массива
        context = super().get_context_data(**kwargs)  # берем существующий контекст
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.name)
        return dict(list(context.items()) + list(c_def.items()))



    def get_queryset(self):
        # print(self.kwargs['cat_slug']) певицы актрисы
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs): # Динамический контекст для передачи динамического массива
        context = super().get_context_data(**kwargs)  # берем существующий контекст
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs): # Динамический контекст для передачи динамического массива
        context = super().get_context_data(**kwargs)  # берем существующий контекст
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')

