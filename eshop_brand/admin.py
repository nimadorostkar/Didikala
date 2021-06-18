import admin_thumbnails
from django.contrib import admin


# Register your models here.
from eshop_brand.models import Brand


@admin_thumbnails.thumbnail('image', 'تصویر برند')
class BrandAdmin(admin.ModelAdmin):
    list_display = ['title', 'title_eng', 'image_thumbnail']
    prepopulated_fields = {'slug': ('title_eng',)}


admin.site.register(Brand, BrandAdmin)