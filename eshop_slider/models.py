from django.db import models
import os
from django.core.exceptions import ValidationError


# برای آپلود عکس و درست کردن آدرسش

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


# برای آپلود عکس و درست کردن آدرسش
def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.title}{ext}"
    return f"sliders/{final_name}"



class Slider(models.Model):
    title = models.CharField('عنوان', max_length=150)
    link = models.URLField('لینک', max_length=150)
    description = models.TextField('توضیحات')
    image = models.ImageField('تصویر', upload_to=upload_image_path, null=True, blank=True)

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدرها'

    def __str__(self):
        return self.title





class SingletonModel(models.Model):
    class Meta:
        abstract = True
    def save(self, *args, **kwargs):
        if not self.pk and self.__class__.objects.exists():
            raise ValidationError('فقط یک نمونه از این مدل می تواند باشد.')
        return super(SingletonModel, self).save(*args, **kwargs)



class BannerRight(SingletonModel):
    title = models.CharField('عنوان', max_length=150)
    link = models.URLField('لینک', max_length=150)
    image = models.ImageField('تصویر', upload_to=upload_image_path, null=True, blank=True)

    class Meta:
        verbose_name = 'بنر راست'
        verbose_name_plural = 'بنر راست'

    def __str__(self):
        return self.title


class BannerLeft(SingletonModel):
    title = models.CharField('عنوان', max_length=150)
    link = models.URLField('لینک', max_length=150)
    image = models.ImageField('تصویر', upload_to=upload_image_path, null=True, blank=True)

    class Meta:
        verbose_name = 'بنر چپ'
        verbose_name_plural = 'بنر چپ'

    def __str__(self):
        return self.title