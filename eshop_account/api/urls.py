from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    UserAddressListCreateAPIView,
    UserAddressUpdateAPIView, OrderListAPIView, OrderDetailAPIView,
    UserProfileAPIViewSet, ProfileCommentListAPIView, ProfileCommentDetailAPIView,
    ProfileHistoryListAPIView, ProfileProductFavouriteUpdateAPIView,
    UserRegisterAPIViewSet, UpdatePassword
)


urlpatterns = [

    path('account/register/', UserRegisterAPIViewSet.as_view(), name='register_api'),
    path('account/login/', obtain_auth_token),
    path('account/change/password/', UpdatePassword.as_view(), name='change_pass_api'),

    path('profile/address/list/', UserAddressListCreateAPIView.as_view(), name='address_list_api'),
    path('profile/address/<int:pk>/', UserAddressUpdateAPIView.as_view(), name='address_api'),
    path('profile/order/list/', OrderListAPIView.as_view(), name='order_list_api'),
    path('profile/order/<int:pk>/', OrderDetailAPIView.as_view(), name='order_detail_api'),
    path('profile/info/<int:pk>/', UserProfileAPIViewSet.as_view(), name='profile_info_api'),
    path('profile/comment/list/', ProfileCommentListAPIView.as_view(), name='profile_comment_list_api'),
    path('profile/comment/<int:pk>/', ProfileCommentDetailAPIView.as_view(), name='profile_comment_delete_api'),
    path('profile/history/list/', ProfileHistoryListAPIView.as_view(), name='profile_history_list_api'),
    path('profile/favourite/list/', ProfileProductFavouriteUpdateAPIView.as_view(), name='profile_favourite_list_api'),


    # path('auth/token/', 'rest_framework_jwt.views.obtain_jwt_token', name='auth_login_api'),
    # path('auth/token/refresh/', 'rest_framework_jwt.views.refresh_jwt_token', name='refresh_token_api'),
]
