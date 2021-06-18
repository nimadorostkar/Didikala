from django.contrib import admin

from eshop_account.models import UserAddress
from eshop_order.models import ShopCart, Order, OrderProduct, PostWay


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'quantity', 'price']
    readonly_fields = ('product', 'user', 'quantity', 'price')


class OrderProductline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product', 'variant', 'price', 'size', 'color', 'quantity', 'amount')
    can_delete = False
    extra = False


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'address_city', 'address_ostsn', 'address_phone', 'amount', 'total_th', 'status',
                    'post_w']
    list_filter = ['status']
    fields = (
        'status', 'admin_note', 'user_name', 'address_full_name', 'address_ostsn', 'address_city', 'address_address',
        'amount', 'total_th', 'post_w', 'post_p', 'ip',)
    readonly_fields = (
        'user_name', 'address_full_name', 'address_ostsn', 'address_city', 'address_address', 'amount', 'total_th',
        'post_w', 'post_p',
        'ip',)
    can_delete = False
    inlines = [OrderProductline]


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'productt', 'image_tag', 'size', 'color', 'price_th', 'quantity', 'amount_th', 'status']
    readonly_fields = (
        'order', 'user', 'productt', 'price_th', 'size', 'color', 'quantity', 'amount_th', 'image_tag')
    fields = (
        'status', 'order', 'user', 'productt', 'size', 'color', 'price_th', 'quantity', 'amount_th', 'image_tag'
    )
    list_filter = ['user']
    can_delete = False


class PostWayAdmin(admin.ModelAdmin):
    list_display = ['way', 'price', 'selected']


admin.site.register(ShopCart, ShopCartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(PostWay, PostWayAdmin)
