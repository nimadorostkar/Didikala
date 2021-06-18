from django.contrib import admin

# Register your models here.
from .models import SiteSetting, FAQ, FAQCategory


class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'update_at', 'status']


class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'update_at', 'status']


class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'mostAsked','status']


admin.site.register(SiteSetting, SiteSettingAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(FAQCategory, FAQCategoryAdmin)
