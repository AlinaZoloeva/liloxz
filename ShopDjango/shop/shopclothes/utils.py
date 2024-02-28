from .models import *

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        categ = Category.objects.all()
        context['categ'] = categ

        return context