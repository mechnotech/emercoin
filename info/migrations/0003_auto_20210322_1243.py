# Generated by Django 3.1.7 on 2021-03-22 12:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0002_auto_20210322_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutemer',
            name='image',
            field=models.ImageField(max_length=150, upload_to='info/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'png', 'svg'])], verbose_name='Изображение блока'),
        ),
        migrations.AlterField(
            model_name='aboutemer',
            name='text',
            field=models.TextField(max_length=500, verbose_name='Описание'),
        ),
    ]
