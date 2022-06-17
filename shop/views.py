from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout


from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Product, Category
from .forms import CreateProductForm
from cart.forms import CartAddProductForm


class CreateProduct(CreateView):
    form_class = CreateProductForm
    model = Product
    template_name = 'shop/create.html'
    success_url = reverse_lazy('home')


class UpdateProduct(UpdateView):
    form_class = CreateProductForm
    model = Product
    template_name = 'shop/update.html'
    success_url = reverse_lazy('home')
    slug_field = 'slug'


class DeleteProduct(DeleteView):
    model = Product
    success_url = reverse_lazy('home')
    slug_field = 'slug'


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


# class ProductDetail(DetailView):
#     """ Информация о продукте """
#     model = Product
#     slug_field = 'slug'
#     template_name = 'shop/product_detail.html'
#     cart_product_form = CartAddProductForm()

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product_detail.html', {'product': product, 'cart_product_form': cart_product_form})

