from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .cart_c import Cart
from .forms import CartAddProductForm
from shop.models import Product


@require_POST # обращение только методом POST
def cart_add(request, product_id):
    cart = Cart(request)  # создаем объект класса Cart
    product = get_object_or_404(Product, id=product_id) # получаем наш продукт
    form = CartAddProductForm(request.POST) #передаем  форму c кол-вом
    if form.is_valid(): # если данные валидны
        cd = form.cleaned_data # помещаем их в чистый словарик
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update']) #обращаемся к методу класса Cart и передаем параметры
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


def cart_detail(request): # информация о корзине
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})
