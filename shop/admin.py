from django.contrib import admin
from django.contrib.gis import forms

from .models import Product, Category, Review
from ckeditor.widgets import CKEditorWidget


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorWidget())

    class Meta:
        model = Product
        fields = '__all__'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'available')
    list_filter = ('available', )
    search_fields = ('title', 'category__name')
    form = ProductAdminForm
    prepopulated_fields = {'slug': ('name',)}





admin.site.register(Category)
admin.site.register(Review)