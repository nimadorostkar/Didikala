from django.urls import path

from eshop_contact.views import contact_page

urlpatterns = [
    path('contact_us', contact_page, name='contact'),

]
