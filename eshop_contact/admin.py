from django.contrib import admin

# Register your models here.
from eshop_contact.models import ContactMessage


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'j_create_at','j_update_at', 'status']
    readonly_fields = ('name', 'subject', 'email', 'message', 'ip')
    list_filter = ['status']


admin.site.register(ContactMessage, ContactMessageAdmin)
