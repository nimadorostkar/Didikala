import os
import random
from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from .signals import object_viewed_signal


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_id = random.randint(1, 999999)
    name, ext = get_filename_ext(filename)
    final_name = f"{new_id}-{instance.user}{ext}"
    return f"users/image/{final_name}"


def upload_gallery_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.user}{ext}"
    return f"user/image/{final_name}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='نام', related_name='profile')
    phone = models.CharField(blank=True, max_length=20, verbose_name='تلفن')
    national_code = models.CharField(blank=True, max_length=20, verbose_name='کدملی', default='_')
    image = models.ImageField(blank=True, null=True, upload_to=upload_image_path, verbose_name='تصویر')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + ' ( ' + self.user.username + ' ) '

    user_name.short_description = 'نام کاربری'

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'تصویر'


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    full_name = models.CharField(blank=True, max_length=60, verbose_name='نام و نام خانوادگی')
    phone = models.CharField(blank=True, max_length=20, verbose_name='تلفن')
    ostan = models.CharField(blank=True, max_length=20, verbose_name='استان')
    city = models.CharField(blank=True, max_length=20, verbose_name='شهر')
    address = models.CharField(blank=True, max_length=150, verbose_name='آدرس پستی')
    post_code = models.IntegerField(blank=True, verbose_name='کد پستی', null=True)
    selected = models.BooleanField(default=False, verbose_name='آدرس منتخب')

    def user_name(self):
        return self.full_name + ' ( ' + self.user.username + ' ) '

    class Meta:
        verbose_name = 'آدرس کاربر'
        verbose_name_plural = 'آدرس کاربران'

    def __str__(self):
        return self.user.username


User = settings.AUTH_USER_MODEL


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)  # product, post
    object_id = models.PositiveIntegerField()  # 1,2,3
    content_object = GenericForeignKey()  # is the actual object
    viewed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s viewed: %s" % (self.content_object, self.viewed_on)

    class Meta:
        verbose_name = 'تاریخ بازدید'
        verbose_name_plural = "تاریخچه بازدیدها"


def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    new_history = History.objects.create(
        user=request.user,
        content_type=ContentType.objects.get_for_model(sender),
        object_id=instance.id,
    )


object_viewed_signal.connect(object_viewed_receiver)

# for rest_framework api
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
