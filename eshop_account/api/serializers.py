from rest_framework import serializers
from django.contrib.auth.models import User
from eshop_account.models import UserProfile, UserAddress, History
from eshop_comment.models import Comment
from eshop_order.models import Order, OrderProduct
from eshop_product.models import Product
from django.contrib.auth.password_validation import validate_password


class UserRegisterSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(style={'input_type': 'password'}, write_only=True, label='تکرار گذرواژه')
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 're_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password = self.validated_data['password']
        re_password = self.validated_data['re_password']

        if password != re_password:
            raise serializers.ValidationError({'password': 'password must match'})
        user.set_password(password)
        user.save()
        user = UserProfile(user=user)
        user.image = 'users/image/avatar.png'
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id',
            "image",
            "phone",
            "national_code",
        ]


class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='profile.phone', allow_null=True, )
    national_code = serializers.CharField(source='profile.national_code', allow_null=True, required=False)
    image = serializers.ImageField(source='profile.image', allow_null=True, default='users/image/avatar.png')
    username = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "image",
            "phone",
            "national_code",
        ]

        related_fields = ['profile']

    def update(self, instance, validated_data):

        for related_obj_name in self.Meta.related_fields:
            # Validated data will show the nested structure
            data = validated_data.pop(related_obj_name)
            related_instance = getattr(instance, related_obj_name)

            # Same as default update implementation
            for attr_name, value in data.items():
                setattr(related_instance, attr_name, value)
            related_instance.save()
        return super(UserSerializer, self).update(instance, validated_data)


class UserAddressListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='address_api')
    user = serializers.CharField()
    full_name = serializers.CharField(required=True)
    ostan = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    post_code = serializers.IntegerField(required=True)

    class Meta:
        model = UserAddress
        fields = [
            "url",
            "id",
            "user",
            "full_name",
            "phone",
            "ostan",
            "city",
            "address",
            "post_code",
            'selected'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.get(username=user_data)
        full_name = validated_data.pop('full_name')
        phone = validated_data.pop('phone')
        ostan = validated_data.pop('ostan')
        city = validated_data.pop('city')
        address = validated_data.pop('address')
        post_code = validated_data.pop('post_code')

        new_address = UserAddress.objects.create(user=user, **validated_data)
        new_address.user = user
        new_address.full_name = full_name
        new_address.phone = phone
        new_address.ostan = ostan
        new_address.city = city
        new_address.address = address
        new_address.post_code = post_code
        new_address.selected = True
        new_address.save()
        user = new_address.user.id
        other_address = UserAddress.objects.filter(user_id=user).exclude(id=new_address.id)
        if other_address:
            for ad in other_address:
                ad.selected = False
                ad.save()
        return new_address


class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    selected = serializers.BooleanField(read_only=True, default=True)

    class Meta:
        model = UserAddress
        fields = [
            "id",
            "user",
            "full_name",
            "phone",
            "ostan",
            "city",
            "address",
            "post_code",
            'selected'
        ]


class ProductSerializerLink1(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='products_detail_api')

    class Meta:
        model = Product
        fields = [
            "title",
            "url",
        ]


class OrderProductListSerializer(serializers.ModelSerializer):
    variant = serializers.CharField(source='variant.title', required=False)
    size = serializers.CharField(source='variant.size', required=False)
    color = serializers.CharField(source='variant.color', required=False)

    product = ProductSerializerLink1(many=False, read_only=True, )

    class Meta:
        model = OrderProduct
        fields = [
            "product",
            "variant",
            "size",
            "color",
            "quantity",
            "price",
            "amount",
            "status",
            "create_at",
            "update_at",
        ]


class OrderDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    products_set = OrderProductListSerializer(source='order', many=True, read_only=True, )
    post_way = serializers.CharField(source='post_way.way', required=False)

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


class OrderListSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    url = serializers.HyperlinkedIdentityField(view_name='order_detail_api')
    post_way = serializers.CharField(source='post_way.way', required=False)

    class Meta:
        model = Order
        fields = [
            "url",
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

        ]


class ProfileCommentDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializerLink1(many=False, read_only=True, )

    class Meta:
        model = Comment
        fields = [
            "product",
            "subject",
            "advantage",
            "disadvantage",
            "comment",
            "advice",
            "status",
            "create_at",
            "update_at",
        ]


class ProfileCommentListSerializer(serializers.ModelSerializer):
    comment_url = serializers.HyperlinkedIdentityField(view_name='profile_comment_delete_api')
    product = serializers.CharField(source='product.title')

    class Meta:
        model = Comment
        fields = [
            "comment_url",
            "product",
            "subject",
            "comment",
            "status",
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            'title',
        )


class ContentObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, Product):
            serializer = ProductSerializer(value)
        else:
            raise Exception('Unexpected type of tagged object')

        return serializer.data


class ProfileHistoryListSerializer(serializers.ModelSerializer):
    content_object = ContentObjectRelatedField(read_only=True)
    user = serializers.CharField(source='user.username')

    class Meta:
        model = History
        fields = [
            "user",
            "content_object",
            "viewed_on",
        ]
        read_only_fields = ('content_object',)


class profileFavouriteListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='products_detail_api')

    class Meta:
        model = Product
        fields = [
            "title",
            "url",
        ]
