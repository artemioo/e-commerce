from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'city', 'address', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    actions = ['paid', 'not_paid']
    inlines = [OrderItemInline]

    def not_paid(self, request, queryset):
        """ Товара не оплачен"""
        row_update = queryset.update(paid=False)
        if row_update == '1':
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f'{row_update} записей было обновлено'
        self.message_user(request, f'{message_bit}')

    def paid(self, request, queryset):
        """ Товар оплачен """
        row_update = queryset.update(paid=True)
        if row_update == '1':
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f'{row_update} записей было обновлено'
        self.message_user(request, f'{message_bit}')

    not_paid.short_description = 'Не оплачен'
    not_paid.allowed_permissions = ('change', )

    paid.short_description = 'Оплачен'
    paid.allowed_permissions = ('change', )