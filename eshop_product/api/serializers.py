from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from eshop_attribute.models import AttrProduct
from eshop_brand.models import Brand
from eshop_image.models import Images
from eshop_product.models import Product, Category
from eshop_comment.models import Comment
from eshop_variant.models import Variants


class VariationSerializerLink(serializers.ModelSerializer):
    color = serializers.CharField(source='color.name', default=None)
    size = serializers.CharField(source='size.name', default=None)

    class Meta:
        model = Variants
        fields = [
            "id",
            "title",
            "color",
            "size",
            "price",
        ]


class ProductSerializer(serializers.ModelSerializer):
    product_url = serializers.HyperlinkedIdentityField(view_name='products_detail_api')

    class Meta:
        model = Product
        fields = [
            'product_url',
            'title',
            'amount',
            'price',
        ]


class ProductSerializerLink(serializers.ModelSerializer):
    product_url = serializers.HyperlinkedIdentityField(view_name='products_detail_api')
    variation_set = VariationSerializerLink(source='variation', many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'title',
            'product_url',
            'price',
            'variation_set',
        ]


class CategorySerializerLink(serializers.HyperlinkedModelSerializer):
    category_url = serializers.HyperlinkedIdentityField(view_name='category_detail_api')

    class Meta:
        model = Category
        fields = [
            'title',
            'category_url',
        ]


class BrandSerializerLink(serializers.ModelSerializer):
    brand_url = serializers.HyperlinkedIdentityField(view_name='brands_api')

    class Meta:
        model = Brand
        fields = [
            'title',
            'brand_url'
        ]


class CommentsSerializerLink(serializers.ModelSerializer):
    user = serializers.CharField(source='user_id.username')

    class Meta:
        model = Comment
        fields = [
            "id",
            "product",
            'user',
            "order_product",
            "subject",
            "advantage",
            "disadvantage",
            "comment",
            "advice",
            "affective_count",
            "notaffective_count",
            "status",
            "create_at",
        ]


class ImagesSerializerLink(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = [
            'image',
        ]


class AttrProductSerializerLink(serializers.ModelSerializer):
    title = serializers.CharField(source='title.title')

    class Meta:
        model = AttrProduct
        fields = [
            "title",
            "rate",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    variation_set = VariationSerializerLink(source='variation', many=True, read_only=True, )
    comment_set = CommentsSerializerLink(source='comment', many=True, read_only=True, )
    gallery_set = ImagesSerializerLink(source='gallery', many=True, read_only=True, )
    attrs_set = AttrProductSerializerLink(source='attrs', many=True, read_only=True, )
    category = CategorySerializerLink(
        many=False,
        read_only=True,
    )
    brand = BrandSerializerLink(
        many=False,
        read_only=True,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "brand",
            "category",
            "variant",
            "price",
            "image",
            "gallery_set",
            "variation_set",
            "attrs_set",
            "comment_set",
        ]


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='category_detail_api')
    # product_set = ProductSerializerLink(many=True, read_only=True, )
    children = RecursiveField(many=True, read_only=True, )

    class Meta:
        model = Category
        fields = [
            'url',
            'id',
            'title',
            'children',
            # 'product_set',
        ]


class BrandDetailSerializer(serializers.ModelSerializer):
    product_set = ProductSerializerLink(many=True, read_only=True, )

    class Meta:
        model = Brand
        fields = [
            'title',
            'product_set'
        ]


class ProductFavouriteUpdateSerializer(serializers.ModelSerializer):
    product_id = serializers.CharField()

    class Meta:
        model = Product
        fields = [
            "product_id",
        ]
