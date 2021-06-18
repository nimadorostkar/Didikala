from django.urls import path
from .views import (
    ProductListAPIViewSet,
    CategoryRetrieveAPIView,
    CategoryListAPIView,
    ProductDetailAPIView,
    BrandDetailAPIViewSet, ProductFavouriteUpdateAPIView,
)

urlpatterns = [
    path('product/list', ProductListAPIViewSet.as_view(), name='products_api'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view(), name='products_detail_api'),
    path('categories/', CategoryListAPIView.as_view(), name='categories_api'),
    path('categories/<int:pk>/', CategoryRetrieveAPIView.as_view(), name='category_detail_api'),
    path('brands/<int:pk>/', BrandDetailAPIViewSet.as_view(), name='brands_api'),
    path('product/favourite/update', ProductFavouriteUpdateAPIView.as_view(), name='product_favourite_update_api'),

]
