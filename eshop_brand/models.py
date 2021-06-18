from django.urls import reverse

from django.db import models
import random
import os


# Create your models here.
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


# برای آپلود عکس و درست کردن آدرسش
def upload_image_path(instance, filename):
    new_id = random.randint(1, 999999)
    name, ext = get_filename_ext(filename)
    final_name = f"{new_id}-{instance.title}{ext}"
    return f"brand/{final_name}"


class Brand(models.Model):
    title = models.CharField(max_length=50, verbose_name='برند')
    title_eng = models.CharField(max_length=150, verbose_name='عنوان انگلیسی')
    keyword = models.CharField(max_length=250, verbose_name='کلمه کلیدی')
    description = models.CharField(max_length=300, verbose_name='توضیحات')
    image = models.ImageField(blank=True, upload_to=upload_image_path, verbose_name='تصویر')
    slug = models.SlugField(verbose_name='عبارت لینک', null=False, unique=True, allow_unicode=True, max_length=200)
    creat_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاده شده در تاریخ')
    update_at = models.DateTimeField(auto_now=True, verbose_name='آپدیت شده در تاریخ')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برندها'

    def get_absolute_url(self):
        return reverse('product_brand_list', kwargs={'slug': self.slug})
