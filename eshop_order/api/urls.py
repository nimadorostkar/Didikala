from django.urls import path

from .views import (
    ShopCartListAPIViewSet,
    ShopCartRetrieveUpdateAPIViewSet, ShopCartCreateAPIViewSet,
    OrderDetailAPIView3
)

urlpatterns = [
    path('cart/list', ShopCartListAPIViewSet.as_view(), name='shop_cart_list_api'),
    path('cart/<int:pk>/', ShopCartRetrieveUpdateAPIViewSet.as_view(), name='shop_cart_detail_api'),
    path('cart/add/', ShopCartCreateAPIViewSet.as_view(),
         name='shop_cart_add_api'),
    path('order/complete/', OrderDetailAPIView3.as_view(), name='order_complete_api'),

]
