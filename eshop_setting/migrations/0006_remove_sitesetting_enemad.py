# Generated by Django 3.2.25 on 2024-12-19 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eshop_setting', '0005_sitesetting_enemad_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitesetting',
            name='enemad',
        ),
    ]
