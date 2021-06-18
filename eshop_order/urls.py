from django.urls import path

from eshop_order.views import (
    addtoshopcart, shopcart, removeshopcart,
    shipping_page, order_completed,
    way_selected, pay_page,
)

urlpatterns = [

    path('cart/add/<int:id>/<int:variantid>', addtoshopcart, name='addToShopCart'),
    path('cart/remove/<int:id>', removeshopcart, name='removeshopcart'),
    path('cart', shopcart, name='ShopCart'),
    path('shipping', shipping_page, name='shipping_page'),
    path('order_complete', order_completed, name='order_completed'),
    path('way_selected/<int:id>', way_selected, name='way_selected'),
    path('payment', pay_page, name='pay_page'),

]
