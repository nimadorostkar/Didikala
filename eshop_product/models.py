import random
from django.contrib.auth.models import User
from django.db import models
import os
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import Q
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.models import MPTTModel
from eshop_brand.models import Brand
from eshop_category.models import Category


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


# برای آپلود عکس و درست کردن آدرسش
def upload_image_path(instance, filename):
    new_id = random.randint(1, 999999)
    name, ext = get_filename_ext(filename)
    final_name = f"{new_id}-{instance.title}{ext}"
    return f"products/{final_name}"


class ProductsManager(models.Manager):
    def get_active_product(self):
        return self.get_queryset().filter(status=True)

    def get_by_id(self, product_id):
        qs = self.get_queryset().filter(id=product_id, status=True)
        if qs.count() == 1:
            return qs.first()
        else:
            return None

    def get_by_categories(self, slug):
        return self.get_queryset().filter(category__in=Category.objects.get(slug=slug) \
                                          .get_descendants(include_self=True), status=True)

    def get_related_product(self, product):
        return self.get_queryset().filter(category__in=Category.objects.get(id=product.id) \
                                          .get_descendants(include_self=True), status=True).exclude(
            id=product.id).distinct()

    def search(self, query):
        lookup = (
                Q(title__icontains=query) |
                Q(title_eng__icontains=query) |
                Q(description__icontains=query) |
                Q(tag__title__icontains=query) |
                Q(category__title__icontains=query)|
                Q(brand__title__icontains=query)
        )
        return self.get_queryset().filter(lookup, status=True).distinct()


class Product(models.Model):
    STATUS = (
        ('True', "فعال"),
        ("False", "غیرفعال")
    )
    VARIANTS = (
        ('None', 'هیچ'),
        ('Size', 'سایز'),
        ('Color', 'رنگ'),
        ('Size-Color', 'سایزـ‌رنگ'),
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='دسته')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='برند')
    title = models.CharField(max_length=200, verbose_name='عنوان فارسی')
    title_eng = models.CharField(max_length=150, blank=True, null=True, verbose_name='عنوان انگلیسی')
    keyword = models.CharField(max_length=250, verbose_name='کلمه کلیدی')
    variant = models.CharField(max_length=10, choices=VARIANTS, default='None', verbose_name='تنوع')
    description = models.CharField(max_length=300, verbose_name='توضیحات')
    image = models.ImageField(upload_to=upload_image_path, verbose_name='تصویر')
    price = models.IntegerField(verbose_name='قیمت')
    amount = models.IntegerField(verbose_name='تعداد')
    all_sale = models.IntegerField(default=0, verbose_name='تعداد فروش')
    view_count = models.BigIntegerField(default=0, verbose_name='تعداد بازدیدها')
    details = RichTextUploadingField(verbose_name='جزئيات محصول')
    analyze = RichTextUploadingField(blank=True, null=True, verbose_name='نقد و بررسی')
    status = models.CharField(max_length=50, choices=STATUS, verbose_name='وضعیت')
    slug = models.SlugField(verbose_name='عبارت لینک', null=False, unique=True, allow_unicode=True, max_length=200)
    creat_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاده شده در تاریخ')
    update_at = models.DateTimeField(auto_now=True, verbose_name='آپدیت شده در تاریخ')
    objects = ProductsManager()

    favourite = models.ManyToManyField(User, blank=True, verbose_name='علاقه‌مندی')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def price_th(self):
        return f"{self.price:,}"

    price_th.short_description = 'قیمت'

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'تصویر'

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug, 'product_id': self.id})

    def get_favourite_url(self):
        return reverse('product_favourite', kwargs={'product_id': self.id})

    def fav_count(self):
        fav = User.objects.filter(product__exact=self.id)
        return fav.count()

    fav_count.short_description = 'تعداد علاقه‌مندان'
