from django.db import models
from extensions.utils import jalali_converter


# Create your models here.

class ContactMessage(models.Model):
    STATUS = (
        ('New', 'جدید'),
        ('Read', 'خوانده شده'),
        ('Closed', 'بسته'),
    )
    name = models.CharField(blank=True, max_length=20, verbose_name='نام و نام‌خانوادگی')
    email = models.CharField(blank=True, max_length=50, verbose_name='ایمیل')
    subject = models.CharField(blank=True, max_length=50, verbose_name='موضوع')
    message = models.TextField(blank=True, max_length=255, verbose_name='پیام')
    status = models.CharField(max_length=10, choices=STATUS, default='New', verbose_name='وضعیت')
    ip = models.CharField(blank=True, max_length=20, verbose_name='آی‌پی')
    note = models.CharField(blank=True, max_length=100, verbose_name='یادداشت')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاده شده در')
    update_at = models.DateTimeField(auto_now=True, verbose_name='آخرین آپدیت')

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'پیام‌‌های مخاطبین'

    def __str__(self):
        return self.subject

    def j_create_at(self):
        return jalali_converter(self.create_at)

    j_create_at.short_description = 'زمان ارسال'

    def j_update_at(self):
        return jalali_converter(self.update_at)

    j_update_at.short_description = 'آخرین آپدیت'
