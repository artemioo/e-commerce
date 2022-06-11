from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout


from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .models import Product, Category



class ProductView(ListView):
    """ Главная страница """
    model = Product
    queryset = Product.objects.filter(available=True)
    template_name = 'base.html'


class CategoryView(ListView):
    """Список категорий"""
    model = Category
    template_name = 'shop/category_list.html'


class Categorize(DetailView):
    """Продукты определенной категории """
    model = Category
    slug_field = 'slug'
    template_name = 'shop/categorize.html'


class ProductDetail(DetailView):
    """ Информация о продукте """
    model = Product
    slug_field = 'slug'
    template_name = 'shop/product_detail.html'


