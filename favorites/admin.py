from django.contrib import admin
from .models import Favorite


@admin.register(Favorite)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added')
