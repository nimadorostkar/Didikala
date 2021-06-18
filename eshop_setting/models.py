import os

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


# برای آپلود عکس و درست کردن آدرسش
def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.title}{ext}"
    return f"logo/{final_name}"


def upload_image_cat_faq_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.title}{ext}"
    return f"faq/{final_name}"


# Create your models here.
class SiteSetting(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    title = models.CharField(max_length=150, verbose_name='عنوان')
    keywords = models.CharField(max_length=255, verbose_name='کلمه کلیدی')
    description = models.CharField(max_length=255, verbose_name='توضیحات')
    company = models.CharField(max_length=50, verbose_name='نام شرکت')
    address = models.CharField(blank=True, max_length=100, verbose_name='آدرس')
    phone = models.CharField(blank=True, max_length=15, verbose_name='تلفن')
    mobile = models.CharField(blank=True, max_length=50, verbose_name='موبایل')
    fax = models.CharField(blank=True, max_length=15, verbose_name='فکس')
    email = models.CharField(blank=True, max_length=50, verbose_name='ایمیل')
    smtpserver = models.CharField(blank=True, max_length=50)
    smtpemail = models.CharField(blank=True, max_length=50)
    smtppassword = models.CharField(blank=True, max_length=10)
    smtpport = models.CharField(blank=True, max_length=5)
    logo = models.ImageField(blank=True, upload_to=upload_image_path, verbose_name='لوگو')
    facebook = models.CharField(blank=True, max_length=50, verbose_name='فیسبوک')
    instagram = models.CharField(blank=True, max_length=50, verbose_name='اینستاگرام')
    twitter = models.CharField(blank=True, max_length=50, verbose_name='توئیتر')
    youtube = models.CharField(blank=True, max_length=50, verbose_name='یوتوب')
    copy_right = models.CharField(max_length=50, verbose_name='کپی رایت')
    aboutus = RichTextUploadingField(blank=True, verbose_name='درباره ما')
    contact = RichTextUploadingField(blank=True, verbose_name='تماس با ما')
    references = RichTextUploadingField(blank=True, verbose_name='رفرنس')
    status = models.CharField(max_length=10, choices=STATUS, verbose_name='وضعیت')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    update_at = models.DateTimeField(auto_now=True, verbose_name='آخرین آپدیت')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات سایت'


class FAQCategory(models.Model):
    STATUS = (
        ('True', "فعال"),
        ("False", "غیرفعال")
    )
    title = models.CharField(max_length=50, verbose_name='عنوان')
    keyword = models.CharField(max_length=250, verbose_name='کلمه کلیدی')
    description = models.CharField(max_length=300, verbose_name='توضیحات')
    image = models.ImageField(upload_to=upload_image_cat_faq_path, verbose_name='تصویر', blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS, verbose_name='وضعیت')
    creat_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاده شده در تاریخ')
    update_at = models.DateTimeField(auto_now=True, verbose_name='آپدیت شده در تاریخ')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته سوال'
        verbose_name_plural = 'دسته‌بندی‌ سوالات'


class FAQ(models.Model):
    STATUS = (
        ('True', 'فعال'),
        ('False', 'غیرفعال'),
    )
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, verbose_name='دسته')
    question = models.CharField(max_length=200, verbose_name='سوال')
    answer = RichTextUploadingField(verbose_name='پاسخ')
    status = models.CharField(max_length=10, choices=STATUS, default='True', verbose_name='وضعیت')
    mostAsked = models.BooleanField(default=False, verbose_name='آیا سوال پرتکرار است؟')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    update_at = models.DateTimeField(auto_now=True, verbose_name='آپدیت در')

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'سوال متداول'
        verbose_name_plural = 'سوالات متداول'
