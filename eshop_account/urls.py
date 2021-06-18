from django.urls import path

from eshop_account import views
from eshop_comment.views import delete_comment
from eshop_account.views import (
    login_user, register, log_out,
    profile_page, product_slider, profile_addresses,
    add_address, remove_address, edit_address,
    selected_address, OrdersList, order_detail,
    profile_sidebar, CommentsList, profile_info,
    profile_info_edit, password_change, HistoryList,
    history_delete, profile_favourites,
)

urlpatterns = [
    path('login', login_user, name='login'),
    path('register', register, name='register'),
    path('logout', log_out, name='logout'),
    path('product_slider', product_slider, name="product_slider"),
    path('profile_page', profile_sidebar, name="profile_sidebar"),
    path('profile', profile_page, name='profile_page'),
    path('profile/info', profile_info, name='profile_info'),
    path('profile/password', password_change, name='password_change'),
    path('profile/info/edit', profile_info_edit, name='profile_info_edit'),
    path('profile/addresses', profile_addresses, name='profile_addresses'),
    path('profile/addresses/add', add_address, name='add_address'),
    path('profile/addresses/edit/<int:id>', edit_address, name='edit_address'),
    path('profile/addresses/remove/<int:id>', remove_address, name='remove_address'),
    path('profile/addresses/selected/<int:id>', selected_address, name='selected_address'),
    path('profile/orders', OrdersList.as_view(), name='OrdersList'),
    path('profile/order/detail/<int:id>', order_detail, name='OrderDetail'),
    path('profile/comments', CommentsList.as_view(), name='CommentsList'),
    path('profile/comment/delete/<int:id>', delete_comment, name='delete_comment'),
    path('profile/history', HistoryList.as_view(), name='historyList'),
    path('profile/history/delete/<int:id>', history_delete, name='history_delete'),
    path('profile/favourites', profile_favourites, name='profile_favourites'),
]
