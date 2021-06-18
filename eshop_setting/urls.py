from django.urls import path

from eshop_setting.views import faq_page, faq_category, faq_question

urlpatterns = [

    path('faq/', faq_page, name='faq_page'),
    path('faq/category/<int:id>', faq_category, name='faq_category'),
    path('faq/question/<int:id>', faq_question, name='faq_question'),

]
