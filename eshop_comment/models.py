from django.contrib.auth.models import User
from django.db import models

from eshop_attribute.models import AttrProduct
from eshop_order.models import OrderProduct
from eshop_product.models import Product
from extensions.utils import jalali_converter


class Comment(models.Model):
    STATUS = (
        ('New', 'در انتظار تائید'),
        ('Submit', 'تائید شده'),
        ('Not_submit', 'تائید نشده'),
    )

    ADVICE = (
        ('yes', 'خرید این محصول را پیشنهاد می‌کنم'),
        ('no', 'خرید این محصول را پیشنهاد نمی‌کنم'),
        ('omm', 'در مورد خرید این محصول نظری ندارم'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comment', verbose_name='نام محصول')
    order_product = models.ForeignKey(OrderProduct, on_delete=models.SET_NULL, blank=True, null=True,
                                      verbose_name='مدل محصول')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='آیدی کاربر', related_name='user_id')
    subject = models.CharField(max_length=50, blank=True, verbose_name='موضوع')
    advantage = models.TextField(blank=True, verbose_name='نقاط قوت', null=True)
    disadvantage = models.TextField(blank=True, verbose_name='نقاط ضعف', null=True)
    comment = models.CharField(max_length=250, blank=True, verbose_name='نظر')
    advice = models.CharField(max_length=100, choices=ADVICE, default='omm', verbose_name='توصیه')
    affective = models.ManyToManyField(User, default=None, blank=True, verbose_name='کامنت مفید',
                                       related_name='affective')
    affective_count = models.BigIntegerField(default='0', verbose_name='تعداد کامنت مفید')
    notaffective = models.ManyToManyField(User, default=None, blank=True, verbose_name='کامنت غیرمفید',
                                          related_name='notaffective')
    notaffective_count = models.BigIntegerField(default='0', verbose_name='تعداد کامنت غیرمفید')
    ip = models.CharField(max_length=20, blank=True, verbose_name='آی‌پی')
    status = models.CharField(max_length=10, choices=STATUS, default='Submit', verbose_name='وضعیت')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاده شده در')
    update_at = models.DateTimeField(auto_now=True, verbose_name='آخرین آپدیت')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'نظرات مشتریان'
        verbose_name_plural = 'نظرات مشتریان'

    def j_create_at(self):
        return jalali_converter(self.create_at)

    j_create_at.short_description = 'زمان ارسال'

    def j_update_at(self):
        return jalali_converter(self.update_at)

    j_update_at.short_description = 'آخرین آپدیت'


class RateComment(models.Model):
    attribute = models.ForeignKey(AttrProduct, on_delete=models.CASCADE, verbose_name='ویژگی')
    rate = models.IntegerField(verbose_name='امتیاز')

    def product(self):
        return self.attribute.product.title

    product.short_description = 'محصول'

    class Meta:
        verbose_name = 'امتیاز'
        verbose_name_plural = 'امتیازات'
