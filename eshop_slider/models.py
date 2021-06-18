from django.db import models
import os


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


# Create your models here.
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
