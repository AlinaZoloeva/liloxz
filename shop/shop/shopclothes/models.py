from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse




class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)
    size = models.TextField()
    price = models.IntegerField()
    color = models.TextField()
    gender = models.ForeignKey('Gender', on_delete=models.PROTECT, null=True)
    count_purch = models.IntegerField(default=0)

    def add_to_cart(self):
        Cart.objects.create(title=self.title, price=self.price, product_code=self)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'det_slug': self.slug})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товар'
        ordering = ['title']

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop', kwargs={'shop_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

class Gender(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop', kwargs={'shop_slug': self.slug})

    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = 'Пол'

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Продукт {self.product.title}'

    def sum(self):
        return self.count * self.product.price

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'

class Coupon(models.Model):
    name = models.TextField()
    percent = models.IntegerField()







