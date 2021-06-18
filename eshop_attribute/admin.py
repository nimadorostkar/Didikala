from django.contrib import admin

# Register your models here.
from eshop_attribute.models import AttrProduct, Attrs


class AttrProductAdmin(admin.ModelAdmin):
    list_display = ['titleAtr', 'product']
    prepopulated_fields = {'slug': ('titleAtr',)}


class AttrsAdmin(admin.ModelAdmin):
    list_display = ['title', ]


admin.site.register(AttrProduct)
admin.site.register(Attrs, AttrsAdmin)
