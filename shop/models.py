from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


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

    def get_review(self):
        return self.review_set.filter(parent__isnull=True) # только родительские отзывы

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})


class Review(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.SET_NULL, null=True)
    text = models.TextField('Сообщение', max_length=1000)
    parent = models.ForeignKey(
        'self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True
    )

    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.product}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

