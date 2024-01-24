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
    gender = models.CharField(max_length=255)
    count_purch = models.IntegerField(default=0)


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