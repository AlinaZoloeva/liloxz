from .models import *
from django.core.cache import cache

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'}]

class DataMixin:
    paginate_by = 2
    def get_user_context(self, **kwargs):
        context = kwargs

        cats = cache.get('cats')

        #if not cats:  если данные не занесены в кэш, то читаем их и заносим
        cats = Category.objects.all()

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu

        context['cats'] = cats

        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context