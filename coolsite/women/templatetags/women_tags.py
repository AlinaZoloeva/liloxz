from django import template
from women.models import *
# Пользовательские теги
register = template.Library()

@register.simple_tag(name="get_cats") #simple tag Возвращает коллекцию
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)


@register.inclusion_tag('women/list_categories.html') # inclusion tag Включающий тег. Возвращает фрагмент шаблона
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {"cats": cats, "cat_selected": cat_selected}

@register.inclusion_tag('women/main.html') # inclusion tag Включающий тег. Возвращает фрагмент шаблона
def show_main():
    return

@register.simple_tag(name="get_posts") #simple tag Возвращает коллекцию
def get_posts(filter=None):
    if not filter:
        return Women.objects.all()
    else:
        return Women.objects.filter(cat_id = filter)