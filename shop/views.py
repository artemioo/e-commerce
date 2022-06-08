from django.http import HttpResponse
from django.shortcuts import render

from .models import Product


def main(request):
    product = Product.objects.all()
    return render(request, 'shop/index.html', {'product': product})
