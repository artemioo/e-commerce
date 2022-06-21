from django.shortcuts import render

from .forms import CreateOrderForm
from .models import OrderItem
from cart.cart_c import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            order = form.save()  #  мы сохраняем его в базу данных, а затем храним в переменной order
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            return render(request, 'orders/successful_create.html', {'order': order})
    form = CreateOrderForm()
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})
