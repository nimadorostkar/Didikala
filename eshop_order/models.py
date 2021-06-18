from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe
from eshop_account.models import UserAddress
from eshop_product.models import Product
from eshop_variant.models import Variants
from extensions.utils import jalali_converter


class PostWay(models.Model):
    way = models.CharField(max_length=60, verbose_name='روش سفارش')
    price = models.IntegerField(verbose_name='هزینه ارسال')
    selected = models.BooleanField(default=False, verbose_name='روش پست منتخب')

    class Meta:
        verbose_name = 'روش‌‌ ارسال'
        verbose_name_plural = 'روش‌های ارسال'

    def __str__(self):
        return self.way


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, verbose_name='محصول')
    variant = models.ForeignKey(Variants, on_delete=models.CASCADE, blank=True, null=True,
                                verbose_name='مدل محصول')  # relation with varinat
    quantity = models.IntegerField(verbose_name='تعداد')

    def __str__(self):
        return self.product.title

    @property
    def price(self):
        if self.variant:
            return f"{self.variant.price:,} تومان "
        else:
            return f"{self.product.price:,} تومان "

    price.fget.short_description = u'قیمت'

    @property
    def amount(self):
        if self.variant:
            return self.quantity * self.variant.price
        else:
            return self.quantity * self.product.price

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'


class Order(models.Model):
    STATUS = (
        ('New', 'جدید'),
        ('Accepted', 'تایید سفارش'),
        ('Preparing', 'آماده سازی سفارش'),
        ('OutCompany', 'خروج از مرکز پردازش'),
        ('InPostOffice', 'تحویل به پست'),
        ('OnShipping', 'مرکز مبادلات پست'),
        ('Arrive', 'تحویل به مشتری'),
        ('Canceled', 'لغو شده'),
    )
    PAY_WAY = (
        ('online', 'پرداخت آنلاین'),
        ('creditCard', 'کیف پول اعتباری')
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='کاربر')
    code = models.CharField(max_length=10, editable=False, verbose_name='کد سفارش')
    address_full_name = models.CharField(blank=True, max_length=60, verbose_name='نام و نام خانوادگی')
    address_phone = models.CharField(blank=True, max_length=20, verbose_name='تلفن')
    address_ostsn = models.CharField(blank=True, max_length=20, verbose_name='استان')
    address_city = models.CharField(blank=True, max_length=20, verbose_name='شهر')
    address_address = models.CharField(blank=True, max_length=150, verbose_name='آدرس پستی')
    address_post_code = models.IntegerField(blank=True, verbose_name='کد پستی', null=True)
    post_way = models.ForeignKey(PostWay, on_delete=models.SET_NULL, null=True, verbose_name='نحوه ارسال')
    pay_way = models.CharField(max_length=50, choices=PAY_WAY, default='online', verbose_name='نحوه پرداخت')
    total = models.IntegerField(verbose_name='جمع مبلغ کل سفارشات')
    amount = models.IntegerField(verbose_name='جمع تعداد کل سفارشات')
    status = models.CharField(max_length=30, choices=STATUS, default='New', verbose_name='وضعیت')
    ip = models.CharField(blank=True, max_length=20, verbose_name='آی‌پی')
    admin_note = models.CharField(blank=True, max_length=100, verbose_name='یادداشت ادمین')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده')
    update_at = models.DateTimeField(auto_now=True, verbose_name='آخرین آپدیت')

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'

    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + ' ( ' + self.user.username + ' ) '

    user_name.short_description = 'نام کاربری'

    def total_th(self):
        return f"{self.total:,}"

    total_th.short_description = 'مبلغ کل'

    def post_w(self):
        return self.post_way.way

    post_w.short_description = 'نحوه ارسال'

    def post_p(self):
        return f"{self.post_way.price:,}"

    post_p.short_description = 'هزینه ارسال'

    def j_create_at(self):
        return jalali_converter(self.create_at)

    j_create_at.short_description = 'زمان ارسال'

    def j_update_at(self):
        return jalali_converter(self.update_at)

    j_update_at.short_description = 'آخرین آپدیت'


class OrderProduct(models.Model):
    STATUS = (
        ('New', 'جدید'),
        ('Accepted', 'تایید سفارش'),
        ('Canceled', 'کنسل سفارش'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سفارش', related_name='order')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='محصول')
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='مدل محصول')
    quantity = models.IntegerField(verbose_name='تعداد')
    price = models.IntegerField(verbose_name='قیمت')
    amount = models.IntegerField(verbose_name='قیمت کل')
    status = models.CharField(max_length=30, choices=STATUS, default='New', verbose_name='وضعیت')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده')
    update_at = models.DateTimeField(auto_now=True, verbose_name='آخرین آپدیت')

    def __str__(self):
        if self.variant:
            return self.variant.title
        else:
            return self.product.title

    class Meta:
        verbose_name = 'سفارش محصول'
        verbose_name_plural = 'سفارشات محصولات'

    def price_th(self):
        return f"{self.price:,}"

    price_th.short_description = 'قیمت'

    def productt(self):
        if self.variant:
            return self.variant.title
        else:
            return self.product.title

    productt.short_description = 'محصول'

    def size(self):
        if self.variant:
            return self.variant.size
        else:
            return f'-'

    size.short_description = 'سایز'

    def color(self):
        if self.variant:
            return self.variant.color
        else:
            return f'-'

    color.short_description = 'رنگ'

    def amount_th(self):
        return f"{self.amount:,}"

    amount_th.short_description = 'قیمت کل'

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.product.image.url))

    image_tag.short_description = 'تصویر'

    def j_create_at(self):
        return jalali_converter(self.create_at)

    j_create_at.short_description = 'زمان ارسال'

    def j_update_at(self):
        return jalali_converter(self.update_at)

    j_update_at.short_description = 'آخرین آپدیت'
