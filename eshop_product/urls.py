from django.urls import path

from eshop_account.views import product_favourite
from eshop_comment.views import comment_page, product_attrs, comment_affective, comment_notaffective
from .views import (
    # category_list,

    search_auto, product_detail, ajaxcolor, product_list_category, search_list,
    product_list_brand,
)

urlpatterns = [

    path('category/<slug>', product_list_category, name='product_category_list'),
    path('brand/<slug>', product_list_brand, name='product_brand_list'),
    path('product_list/search', search_list, name='search_list'),
    path('search_auto/', search_auto, name='search_auto'),
    path('product_detail/<product_id>/<slug>', product_detail, name='product_detail'),
    path('product/favourite/<product_id>', product_favourite, name='product_favourite'),
    path('product/comment/<int:id>', comment_page, name='comment_product'),
    path('product/comment/affective', comment_affective, name='comment_affective'),
    path('product/comment/notaffective', comment_notaffective, name='comment_notaffective'),
    path('product/rate_comment/<int:product_id>/<slug>', product_attrs, name='product_attrs'),
    path('ajaxcolor/', ajaxcolor, name='ajaxcolor'),

]
