from django.db import models

# Create your models here.
from eshop_product.models import Product


class Tag(models.Model):
    STATUS = (
        ('True', "فعال"),
        ("False", "غیرفعال")
    )
    title = models.CharField(max_length=120, verbose_name='عنوان')
    product = models.ManyToManyField(Product, blank=True, verbose_name='محصول')
    status = models.CharField(max_length=50, choices=STATUS, verbose_name='وضعیت', default=True)
    slug = models.SlugField(verbose_name='عبارت لینک', unique=True, null=False, allow_unicode=True, max_length=200)
    creat_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاده شده در تاریخ')
    update_at = models.DateTimeField(auto_now=True, verbose_name='آپدیت شده در تاریخ')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'برچسب'
        verbose_name_plural = 'برچسب‌ها'
