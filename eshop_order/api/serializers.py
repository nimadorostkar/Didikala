from rest_framework import serializers
from eshop_account.api.serializers import OrderProductListSerializer
from eshop_order.models import ShopCart, Order

class ShopCartListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='shop_cart_detail_api')
    user = serializers.CharField(source='user.username', required=False)
    product = serializers.CharField(source='product.title', required=False)
    variant_title = serializers.CharField(source='variant.title', default=None)
    variant_color = serializers.CharField(source='variant.color', default=None)
    variant_size = serializers.CharField(source='variant.size', default=None)
    quantity = serializers.IntegerField(required=False)

    class Meta:
        model = ShopCart
        fields = [
            "url",
            "user",
            'product',
            "variant_title",
            "variant_color",
            "variant_size",
            "quantity",
            "price",
            "amount",

        ]


class ShopCartUpdateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True, )
    product = serializers.CharField(source='product.title', read_only=True, )
    variant_title = serializers.CharField(source='variant.title', default=None, required=False, read_only=True, )
    variant_color = serializers.CharField(source='variant.color', default=None, read_only=True, )
    variant_size = serializers.CharField(source='variant.size', default=None, read_only=True, )
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = ShopCart
        fields = [
            "user",
            'product',
            "variant_title",
            "variant_color",
            "variant_size",
            "quantity",
            "price",
            "amount",

        ]


class ShopCartAddSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    product_id = serializers.IntegerField(required=True)
    variant_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField()

    class Meta:
        model = ShopCart
        fields = [
            "user",
            'product_id',
            "variant_id",
            "quantity",
        ]

    # def create(self, validated_data):
    #     product_data = validated_data.pop('product')
    #     quantity_data = validated_data.pop('quantity')
    #     user_data = validated_data.pop('user_id')
    #     try:
    #         product = Product.objects.get(id=product_data)
    #         user = User.objects.get(id=user_data)
    #     except Product.DoesNotExist:
    #         pass
    #
    #     if product.variant != 'None':
    #         variant_data = validated_data.pop('variant')
    #         variant = Variants.objects.get(id=variant_data)
    #         checkinvariant = ShopCart.objects.filter(variant_id=variant.id,
    #                                                  user_id=user.id)  # Check product in shopcart
    #         if checkinvariant:
    #             control = 1  # The product is in the cart
    #         else:
    #             control = 0  # The product is not in the cart
    #     else:
    #         checkinproduct = ShopCart.objects.filter(product_id=product.id,
    #                                                  user_id=user.id)  # Check product in shopcart
    #         if checkinproduct:
    #             control = 1  # The product is in the cart
    #         else:
    #             control = 0  # The product is not in the cart
    #
    #     if control == 1:
    #         if product.variant == 'None':
    #             instance = ShopCart.objects.get(product_id=product.id, user_id=user.id)
    #         else:
    #             instance = ShopCart.objects.get(product_id=product.id, variant_id=variant.id, user_id=user.id)
    #         instance.quantity += quantity_data
    #         instance.save()  # save data
    #
    #     else:
    #         instance = ShopCart.objects.create(quantity=quantity_data, **validated_data)
    #         instance.user = user
    #         instance.product = product
    #         instance.quantity = quantity_data
    #         if product.variant == 'None':
    #             instance.variant = None
    #         else:
    #             instance.variant = variant
    #         instance.save()
    #     return instance


class OrderCreatDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True, )
    post_way_id = serializers.IntegerField(required=True)

    class Meta:
        model = Order
        fields = [
            "user",
            "post_way_id",
        ]


class OrderDetailSerializer1(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True, )
    products_set = OrderProductListSerializer(source='order', many=True, read_only=True, )
    total = serializers.IntegerField(required=False)
    amount = serializers.IntegerField(required=False)
    post_way = serializers.CharField(source='post_way.way', required=True)

    class Meta:
        model = Order
        fields = [
            "user",
            "code",
            "address_full_name",
            "address_phone",
            "address_ostsn",
            "address_city",
            "address_address",
            "address_post_code",
            "post_way",
            "pay_way",
            "total",
            "amount",
            "status",
            "ip",
            "admin_note",
            "create_at",
            "update_at",
            "products_set"

        ]
