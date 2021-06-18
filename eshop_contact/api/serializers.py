from rest_framework import serializers
from eshop_contact.models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    subject = serializers.CharField(required=True)
    message = serializers.CharField(required=True)

    class Meta:
        model = ContactMessage
        fields = [
            "name",
            "email",
            "subject",
            "message",
        ]


class ContactMessageListAdminSerializer(serializers.ModelSerializer):
    massage_url = serializers.HyperlinkedIdentityField(view_name='contact_massage_detail_api')

    class Meta:
        model = ContactMessage
        fields = [
            "massage_url",
            "name",
            "subject",
            "status",
            "create_at",
        ]


class ContactMessageDetailAdminSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True, )
    email = serializers.CharField(read_only=True, )
    subject = serializers.CharField(read_only=True, )
    message = serializers.CharField(read_only=True, )
    status = serializers.ChoiceField(choices=['New', 'Read', 'Closed'])

    class Meta:
        model = ContactMessage
        fields = [
            "id",
            "name",
            "email",
            "subject",
            "message",
            "status",
            "note",
            "ip",
            "create_at",
            "update_at",
        ]
