# Generated by Django 3.1.7 on 2021-04-13 14:58

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0034_privacy_terms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privacy',
            name='text',
            field=ckeditor.fields.RichTextField(max_length=50000, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='privacy',
            name='text_en',
            field=ckeditor.fields.RichTextField(max_length=50000, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='terms',
            name='text',
            field=ckeditor.fields.RichTextField(max_length=50000, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='terms',
            name='text_en',
            field=ckeditor.fields.RichTextField(max_length=50000, verbose_name='Description'),
        ),
    ]
