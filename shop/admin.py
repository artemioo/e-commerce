from django.contrib import admin
from .models import Product, Category, Review


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'available')
    list_filter = ('available', )
    search_fields = ('title', 'category__name')

    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category)
admin.site.register(Review)