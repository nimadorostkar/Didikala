import admin_thumbnails
from django.contrib import admin

# Register your models here.
from eshop_image.models import Images


# Image model
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'image_tag']


admin.site.register(Images, ImageAdmin)
