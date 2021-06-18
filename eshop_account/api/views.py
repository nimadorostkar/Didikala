from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions, generics
from django.contrib.auth.models import User
from eshop_account.models import UserProfile, UserAddress, History
from eshop_comment.models import Comment
from eshop_order.models import Order
from eshop_product.models import Product
from eshop_account.api.serializers import (
    UserRegisterSerializer, UserProfileSerializer, UserAddressSerializer,
    UserAddressListSerializer, OrderListSerializer, OrderDetailSerializer,
    UserSerializer, ProfileCommentListSerializer, ProfileCommentDetailSerializer,
    ProfileHistoryListSerializer, profileFavouriteListSerializer, ChangePasswordSerializer,
)


class UserRegisterAPIViewSet(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()


class UpdatePassword(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(data='پسورد با موفقیت تغییر یافت. لطفا دوباره لاگین کنید',
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIViewSet(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class UserAddressListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = UserAddressListSerializer
    queryset = UserAddress.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return UserAddress.objects.filter(user__username=self.request.user.username)


class UserAddressUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserAddressSerializer
    queryset = UserAddress.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return UserAddress.objects.filter(user__username=self.request.user.username)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.selected = True
        instance.save()
        serializer = self.get_serializer(instance, data=request.data)
        other_add = UserAddress.objects.filter(user__username=self.request.user.username).exclude(id=instance.id)
        for ad in other_add:
            ad.selected = False
            ad.save()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        add = self.get_object()
        add.delete()

        return Response(data='delete success')


class OrderListAPIView(generics.ListAPIView):
    serializer_class = OrderListSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Order.objects.filter(user__username=self.request.user.username).order_by("-id")


class OrderDetailAPIView(generics.RetrieveAPIView):
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Order.objects.filter(user__username=self.request.user.username)


class ProfileCommentListAPIView(generics.ListAPIView):
    serializer_class = ProfileCommentListSerializer
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Comment.objects.filter(user_id=self.request.user)


class ProfileCommentDetailAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = ProfileCommentDetailSerializer
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Comment.objects.filter(user_id=self.request.user)

    # def destroy(self, request, *args, **kwargs):
    #     comment = self.get_object()
    #     comment.delete()
    #     return Response(data='delete success')


class ProfileHistoryListAPIView(generics.ListAPIView):
    serializer_class = ProfileHistoryListSerializer
    queryset = History.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return History.objects.filter(user_id=self.request.user).order_by('-id')[:30]


class ProfileProductFavouriteUpdateAPIView(generics.ListAPIView):
    serializer_class = profileFavouriteListSerializer
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Product.objects.filter(favourite=self.request.user)[:30]


# Admin API
class AccountListAPIViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return UserProfile.objects.filter(pk=self.request.user.profile.pk)
