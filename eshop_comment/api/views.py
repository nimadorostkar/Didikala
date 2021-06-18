from django.contrib.auth.models import User
from django.db.models import Avg
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from eshop_attribute.models import AttrProduct
from eshop_comment.api.serializers import CommentSerializer, RateCommentSerializer, CommentAffectSerializer
from eshop_comment.models import Comment, RateComment
from eshop_product.models import Product


class CommentCreateAPIViewSet(generics.CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class RateCommentAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = RateCommentSerializer
    queryset = RateComment.objects.all()

    def post(self, request, format=None):
        serializer = RateCommentSerializer(data=request.data)
        if serializer.is_valid():
            current_user = User.objects.get(id=request.data['user_id'])
            product = Product.objects.get(id=request.data['product_id'])
            attr = AttrProduct.objects.get(slug__exact=request.data['attribute_slug'], product__exact=product)

            data = RateComment()
            data.attribute = attr
            data.rate = int(request.data['rate'])
            data.save()
            all_rate_comment = RateComment.objects.filter(attribute=attr).aggregate(avarage=Avg('rate'))
            avg = 0
            if all_rate_comment["avarage"] is not None:
                avg = int(all_rate_comment["avarage"])
                attr.rate = avg
                attr.save()
        if serializer.errors:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data='امتیاز ثبت شد', status=status.HTTP_201_CREATED)


class AffectiveCommentAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = CommentAffectSerializer
    queryset = Comment.objects.all()

    def post(self, request, format=None):
        serializer = CommentAffectSerializer(data=request.data)
        if serializer.is_valid():
            current_user = User.objects.get(id=request.data['user_id'])
            comment = Comment.objects.filter(id=request.data['comment_id']).first()

            if comment.notaffective.filter(id=current_user.id).exists():
                comment.notaffective.remove(current_user.id)
                comment.notaffective_count -= 1
                comment.affective.add(current_user.id)
                comment.affective_count += 1
                comment.save()

            if comment.affective.filter(id=current_user.id).exists():
                pass

            else:
                comment.affective.add(current_user.id)
                comment.affective_count += 1
                comment.save()
        if serializer.errors:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data='این نظر مفید بوده است', status=status.HTTP_200_OK)


class NotAffectiveCommentAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = CommentAffectSerializer
    queryset = Comment.objects.all()

    def post(self, request, format=None):
        serializer = CommentAffectSerializer(data=request.data)
        if serializer.is_valid():
            current_user = User.objects.get(id=request.data['user_id'])
            comment = Comment.objects.filter(id=request.data['comment_id']).first()

            if comment.affective.filter(id=current_user.id).exists():
                comment.affective.remove(current_user.id)
                comment.affective_count -= 1

                comment.notaffective.add(current_user.id)
                comment.notaffective_count += 1
                comment.save()

            if comment.notaffective.filter(id=current_user.id).exists():
                pass
            else:
                comment.notaffective.add(current_user.id)
                comment.notaffective_count += 1
                comment.save()

        if serializer.errors:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data='این نظر مفید نبوده است', status=status.HTTP_200_OK)
