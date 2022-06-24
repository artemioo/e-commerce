from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Avg, Max

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
        # mb refactor it's
        # if max_price or max_price == '':
        #     min_price = 1
        #     max_price = Product.objects.aggregate(Max('price'))['price__max']

        if search_query:
            queryset = Product.objects.filter(name__icontains=search_query)
        elif category_query:
            queryset = Product.objects.filter(category__in=category_query)
        elif max_price or min_price:
            queryset = Product.objects.filter(price__range=(min_price, max_price))
        else:
            queryset = Product.objects.filter(available=True)
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

