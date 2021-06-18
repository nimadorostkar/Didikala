from django.urls import path

from .views import (
    ContactMessageCreateAPIViewSet,
    ContactMessageListAPIViewSet,
    ContactMessageRetrieveUpdateAPIView,

)

urlpatterns = [

    path('contact_us/', ContactMessageCreateAPIViewSet.as_view(), name='contact_massage_api'),

    # Admin api
    path('admin/contact_us/list', ContactMessageListAPIViewSet.as_view(), name='contact_massage_list_api'),
    path('admin/contact_us/<int:pk>/', ContactMessageRetrieveUpdateAPIView.as_view(), name='contact_massage_detail_api'),

]
