from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from eshop_contact.models import ContactMessage
from eshop_product.api.pagination import ProductPagination
from eshop_contact.api.serializers import (
    ContactMessageSerializer,
    ContactMessageListAdminSerializer,
    ContactMessageDetailAdminSerializer,
)


class ContactMessageCreateAPIViewSet(generics.CreateAPIView):
    serializer_class = ContactMessageSerializer
    queryset = ContactMessage.objects.all()

    def post(self, request, format=None):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            name = request.data['name']
            email = request.data['email']
            subject = request.data['subject']
            message = request.data['message']
            ip = request.META.get('REMOTE_ADDR')
            contact_massage = ContactMessage()
            contact_massage.name = name
            contact_massage.email = email
            contact_massage.subject = subject
            contact_massage.message = message
            contact_massage.ip = ip
            contact_massage.save()
        if serializer.errors:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data='پیام شما با موفقیت ارسال شد', status=status.HTTP_201_CREATED)


# Admin api
class ContactMessageListAPIViewSet(generics.ListAPIView):
    serializer_class = ContactMessageListAdminSerializer
    queryset = ContactMessage.objects.all()
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [TokenAuthentication]
    pagination_class = ProductPagination


class ContactMessageRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContactMessageDetailAdminSerializer
    queryset = ContactMessage.objects.all()
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [TokenAuthentication]
