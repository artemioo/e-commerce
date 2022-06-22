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
    actions = ['available', 'unavailable']
    form = ProductAdminForm
    prepopulated_fields = {'slug': ('name',)}

    def unavailable(self, request, queryset):
        """ Товара нет в наличии или он недоступен"""
        row_update = queryset.update(available=False)
        if row_update == '1':
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f'{row_update} записей было обновлено'
        self.message_user(request, f'{message_bit}')

    def available(self, request, queryset):
        """ Товара в наличии """
        row_update = queryset.update(available=True)
        if row_update == '1':
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f'{row_update} записей было обновлено'
        self.message_user(request, f'{message_bit}')

    unavailable.short_description = 'Нет в наличии'
    unavailable.allowed_permissions = ('change', )

    available.short_description = 'В наличии'
    available.allowed_permissions = ('change', )


admin.site.register(Category)
admin.site.register(Review)
