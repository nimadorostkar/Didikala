from django.utils.crypto import get_random_string
from rest_framework.response import Response
from rest_framework import status
from eshop_account.models import UserAddress
from eshop_product.models import Product
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from eshop_order.api.serializers import ShopCartListSerializer, ShopCartUpdateSerializer, ShopCartAddSerializer, \
    OrderCreatDetailSerializer, OrderDetailSerializer1
from eshop_order.models import ShopCart, Order, PostWay, OrderProduct
from rest_framework import generics
from eshop_variant.models import Variants


class ShopCartListAPIViewSet(generics.ListAPIView):
    serializer_class = ShopCartListSerializer
    queryset = ShopCart.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return ShopCart.objects.filter(user__username=self.request.user.username)

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = ShopCartListSerializer(queryset, many=True, context={'request': request})
        totalPrice = 0
        totalCount = 0
        for rs in serializer.data:
            totalPrice += int(rs['amount'])
            totalCount += int(rs['quantity'])

        data = {
            'shopcart': serializer.data,
            'totalPrice': totalPrice,
            'totalCount': totalCount
        }
        return Response(data)


class ShopCartRetrieveUpdateAPIViewSet(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ShopCartUpdateSerializer
    queryset = ShopCart.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return ShopCart.objects.filter(user__username=self.request.user.username)


class ShopCartCreateAPIViewSet(generics.CreateAPIView):
    serializer_class = ShopCartAddSerializer
    queryset = ShopCart.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = ShopCartAddSerializer(data=request.data)
        if serializer.is_valid():
            product_data = request.data['product_id']
            quantity_data = int(request.data['quantity'])
            user = self.request.user
            product = Product.objects.get(id=product_data)

            if product.variant != 'None':
                variant_data = request.data['variant_id']
                variant = Variants.objects.get(id=variant_data)
                if variant.quantity >= quantity_data:
                    pass
                else:
                    return Response(data=f"تعداد شفارش باید کمتر از {variant.quantity} باشد ",
                                    status=status.HTTP_400_BAD_REQUEST)

            else:
                if product.amount >= quantity_data:
                    pass
                else:
                    return Response(data=f"تعداد شفارش باید کمتر از {product.amount} باشد ",
                                    status=status.HTTP_400_BAD_REQUEST)

            if product.variant != 'None':
                variant_data = request.data['variant_id']
                variant = Variants.objects.get(id=variant_data)
                checkinvariant = ShopCart.objects.filter(variant_id=variant.id,
                                                         user_id=user.id)  # Check product in shopcart
                if checkinvariant:
                    control = 1  # The product is in the cart
                else:
                    control = 0  # The product is not in the cart
            else:
                checkinproduct = ShopCart.objects.filter(product_id=product.id,
                                                         user_id=user.id)  # Check product in shopcart
                if checkinproduct:
                    control = 1  # The product is in the cart
                else:
                    control = 0  # The product is not in the cart

            if control == 1:
                if product.variant == 'None':
                    instance = ShopCart.objects.get(product_id=product.id, user_id=user.id)
                else:
                    instance = ShopCart.objects.get(product_id=product.id, variant_id=variant.id, user_id=user.id)

                instance.quantity += quantity_data
                instance.save()  # save data

            else:
                instance = ShopCart()
                instance.user = user
                instance.product = product
                instance.quantity = quantity_data
                if product.variant == 'None':
                    instance.variant = None
                else:
                    instance.variant = variant
                instance.save()
        if serializer.errors:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ShopCartUpdateSerializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailAPIView3(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = OrderCreatDetailSerializer
    queryset = Order.objects.all()

    def post(self, request, format=None):
        serializer = OrderCreatDetailSerializer(data=request.data)
        if serializer.is_valid():
            current_user = self.request.user
            selected_address = UserAddress.objects.get(user__username=current_user, selected=True)
            selected_post_way = PostWay.objects.get(id=request.data['post_way_id'])
            shopcart = ShopCart.objects.filter(user_id=current_user.id)
            if shopcart:
                totalPrice = 0
                totalCount = 0
                totalPriceWithPost = 0
                for rs in shopcart:
                    totalPrice += rs.amount
                    totalCount += rs.quantity
                    totalPriceWithPost = totalPrice + selected_post_way.price

                data = Order()
                data.user = current_user  # get product quantity from form
                data.address_address = selected_address.address
                data.address_full_name = selected_address.full_name
                data.address_phone = selected_address.phone
                data.address_ostsn = selected_address.ostan
                data.address_city = selected_address.city
                data.address_post_code = selected_address.post_code
                data.post_way = selected_post_way
                data.total = totalPriceWithPost
                data.amount = totalCount
                data.ip = request.META.get('REMOTE_ADDR')
                ordercode = get_random_string(10).upper()  # random cod
                data.code = ordercode
                data.save()

                for rs in shopcart:
                    detail = OrderProduct()
                    detail.order_id = data.id  # Order Id
                    detail.product_id = rs.product_id
                    detail.user_id = current_user.id
                    detail.quantity = rs.quantity
                    detail.amount = rs.amount

                    variants = Variants.objects.filter(product_id=rs.product_id)
                    if rs.product.variant == 'None' or variants.count() == 0:
                        detail.price = rs.product.price
                    else:
                        detail.price = rs.variant.price
                    detail.variant_id = rs.variant_id
                    detail.save()

                    if rs.product.variant == 'None' or variants.count() == 0:
                        product = Product.objects.get(id=rs.product_id)
                        product.amount -= rs.quantity
                        product.all_sale += rs.quantity
                        product.save()
                    else:
                        variant = Variants.objects.get(id=rs.variant_id)
                        product = Product.objects.get(id=rs.product_id)
                        variant.quantity -= rs.quantity
                        product.all_sale += rs.quantity
                        variant.save()
                        product.save()
                ShopCart.objects.filter(user_id=current_user.id).delete()  # Clear & Delete shopcart
                serializer = OrderDetailSerializer1(data, context={'request': request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data='ShopCart is empty', status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
