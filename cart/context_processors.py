from .cart_c import Cart


def cart(request):
    return {'cart': Cart(request)}
