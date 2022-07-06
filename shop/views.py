from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Product, Category
from .forms import CreateProductForm, ReviewForm
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
    template_name = 'base.html'
    paginate_by = 2

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        category_query = self.request.GET.get('category', '')
        min_price = self.request.GET.get('min_price', 0)
        max_price = self.request.GET.get('max_price', 0)

        if search_query:
            queryset = Product.objects.filter(name__icontains=search_query)
        elif category_query:
            queryset = Product.objects.filter(category__in=category_query)
        elif max_price or min_price:
            queryset = Product.objects.filter(price__range=(min_price, max_price))
        else:
            queryset = Product.objects.filter(available=True).select_related('category')

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('search', '')
        context['categories'] = Category.objects.all()
        return context


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

    def get(self, request, *args, **slug):
        self.slug_field = slug[self.slug_field]

        if cache.get(self.slug_field):
            self.product = cache.get(self.slug_field)
        else:
            self.product = get_object_or_404(self.model, slug=self.slug_field)
            cache.set(self.slug_field, self.product)

        cart_product_form = CartAddProductForm()
        context = {
            'product': self.product,
            'cart_product_form': cart_product_form
        }
        return self.render_to_response(context)


class AddReview(View):
    """ Отзывы к товару """
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        product = Product.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.product = product
            form.user = request.user
            form.save()
        return redirect(product.get_absolute_url())

