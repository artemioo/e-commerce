from django.db import models
from django.urls import reverse


class Category(models.Model):
    """ Категории товаров """
    name = models.CharField('Категория', max_length=150)
    slug = models.SlugField(max_length=150, unique=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('categorize', kwargs={'slug': self.slug})


class Product(models.Model):
    """ Товар """
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    name = models.CharField('Название товара', max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    image = models.ImageField('Изображение', upload_to='shop/')
    description = models.TextField('Описание', max_length=1000, blank=True)
    price = models.DecimalField('Цена', max_digits=15, decimal_places=2)
    available = models.BooleanField('В Наличии', default=True)
    created = models.DateTimeField('Добавлено', auto_now_add=True)
    uploaded = models.DateTimeField('Измененно', auto_now=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        indexes = [models.Index(fields=['name', 'slug'])]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})
