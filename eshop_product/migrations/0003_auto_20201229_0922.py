# Generated by Django 3.1 on 2020-12-29 05:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eshop_brand', '0001_initial'),
        ('eshop_category', '0003_auto_20201214_1209'),
        ('eshop_product', '0002_product_favourite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='eshop_brand.brand', verbose_name='برند'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='eshop_category.category', verbose_name='دسته'),
        ),
    ]
