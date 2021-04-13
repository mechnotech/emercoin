# Generated by Django 3.1.7 on 2021-04-13 14:55

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0033_auto_20210413_1446'),
    ]

    operations = [
        migrations.CreateModel(
            name='Privacy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Заголовок')),
                ('title_en', models.CharField(max_length=50, verbose_name='Title')),
                ('date', models.DateTimeField(verbose_name='Дата и время')),
                ('text', ckeditor.fields.RichTextField(max_length=30000, verbose_name='Описание')),
                ('text_en', ckeditor.fields.RichTextField(max_length=30000, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Privacy Policy',
                'verbose_name_plural': 'Privacy Policy',
            },
        ),
        migrations.CreateModel(
            name='Terms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Заголовок')),
                ('title_en', models.CharField(max_length=50, verbose_name='Title')),
                ('date', models.DateTimeField(verbose_name='Дата и время')),
                ('text', ckeditor.fields.RichTextField(max_length=30000, verbose_name='Описание')),
                ('text_en', ckeditor.fields.RichTextField(max_length=30000, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Термс',
                'verbose_name_plural': 'Emercoin and Conditions',
            },
        ),
    ]
