from django.urls import path
from .views import (
    CommentCreateAPIViewSet,
    RateCommentAPIView,
    AffectiveCommentAPIView,
    NotAffectiveCommentAPIView,
)

urlpatterns = [

    path('product/comment/', CommentCreateAPIViewSet.as_view(), name='comment_product_api'),
    path('product/rate_comment/', RateCommentAPIView.as_view(), name='product_attrs_rate_api'),
    path('product/affective_comment/', AffectiveCommentAPIView.as_view(), name='affective_comment_api'),
    path('product/not_affective_comment/', NotAffectiveCommentAPIView.as_view(), name='not_affective_comment_api'),

]
