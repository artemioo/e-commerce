from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Product, Review


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'name', 'slug', 'image', 'description', 'price', 'available')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('text', )

