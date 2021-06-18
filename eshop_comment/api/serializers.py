from rest_framework import serializers
from eshop_comment.models import Comment, RateComment
from eshop_order.models import OrderProduct
from eshop_product.models import Product


class CommentSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    subject = serializers.CharField(required=True)
    advantage = serializers.CharField(required=False)
    disadvantage = serializers.CharField(required=False)
    comment = serializers.CharField(required=True)
    advice = serializers.ChoiceField(choices=['yes', 'no', 'omm'], required=True)
    order_product = serializers.CharField(source='order_product.productt', required=False)

    class Meta:
        model = Comment
        fields = [

            "product_id",
            "order_product",
            "user_id",
            "subject",
            "advantage",
            "disadvantage",
            "comment",
            "advice",
            "ip",
            "status",
            "create_at",
            "update_at",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user_id')
        product = validated_data.pop('product_id')
        product = Product.objects.get(id=product)
        subject = validated_data.pop('subject')
        advantage = validated_data.pop('advantage', None)
        disadvantage = validated_data.pop('disadvantage', None)
        comment = validated_data.pop('comment')
        advice = validated_data.pop('advice')
        ip = self.context.get('request').META.get("REMOTE_ADDR")

        new_comment = Comment.objects.create(user_id=user_data, product_id=product.id, **validated_data)
        new_comment.user_id = user_data
        new_comment.subject = subject
        new_comment.advantage = advantage
        new_comment.disadvantage = disadvantage
        new_comment.comment = comment
        new_comment.advice = advice
        new_comment.ip = ip
        if OrderProduct.objects.filter(user_id=user_data, product_id=product.id).exists():
            new_comment.order_product = OrderProduct.objects.filter(user_id=user_data, product_id=product.id).first()
        new_comment.save()
        return new_comment


class CommentAffectSerializer(serializers.ModelSerializer):
    comment_id = serializers.CharField(write_only=True, required=True)
    user_id = serializers.CharField(write_only=True,  required=True)

    class Meta:
        model = Comment
        fields = [
            "comment_id",
            "user_id",
        ]


class RateCommentSerializer(serializers.ModelSerializer):
    product_id = serializers.CharField(write_only=True, required=True)
    attribute_slug = serializers.CharField(write_only=True, required=True)
    user_id = serializers.CharField(write_only=True, required=True)
    rate = serializers.IntegerField(max_value=5, min_value=0, required=True)

    class Meta:
        model = RateComment
        fields = [
            "user_id",
            "product_id",
            "attribute_slug",
            "rate",
        ]
