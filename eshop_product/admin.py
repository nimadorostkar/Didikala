import admin_thumbnails
from django.contrib import admin

from eshop_attribute.models import AttrProduct
from eshop_image.models import Images
from eshop_tag.models import Tag
from eshop_variant.models import Variants
from .models import Product
from django.contrib import messages
from django.utils.translation import ngettext


class AttrProductInline(admin.TabularInline):
    model = AttrProduct
    prepopulated_fields = {'slug': ('title',)}
    extra = 1


@admin_thumbnails.thumbnail('image', 'تصویر')
class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1


@admin_thumbnails.thumbnail('image', 'تصویر')
class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1


@admin_thumbnails.thumbnail('image', 'تصویر')
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['image', 'title', 'image_thumbnail']


class TagInline(admin.StackedInline):
    model = Tag.product.through
    extra = 1


class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True


# first way for admin action
def make_active(modeladmin, request, queryset):
    updated = queryset.update(status='True')
    modeladmin.message_user(request, ngettext(
        '%d محصول فعال شد.',
        '%d محصول فعال شد.',
        updated,
    ) % updated, messages.SUCCESS)


make_active.short_description = "فعال کردن محصول انتخابی"


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'brand', 'image_tag', 'price_th', 'amount', 'all_sale', 'category', 'tag_list', 'status']
    list_filter = ['category']
    list_editable = ['brand']
    readonly_fields = ["image_tag", 'all_sale', 'view_count']
    inlines = [ProductImageInline, ProductVariantsInline, TagInline, AttrProductInline]
    prepopulated_fields = {'slug': ('title',)}
    actions = [make_active, 'make_not_active']

    def tag_list(self, obj):
        return ' ، '.join([tag.title for tag in Tag.objects.filter(product=obj, status=True)])

    tag_list.short_description = 'برچسب'

    # second way for admin action
    def make_not_active(self, request, queryset):
        updated = queryset.update(status='False')
        self.message_user(request, ngettext(
            '%d محصول غیرفعال شد.',
            '%d محصول غیرفعال شد.',
            updated,
        ) % updated, messages.SUCCESS)

    make_not_active.short_description = "غیرفعال کردن محصول انتخابی"


admin.site.register(Product, ProductAdmin)
