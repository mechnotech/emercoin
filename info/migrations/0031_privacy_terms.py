# Generated by Django 3.1.7 on 2021-04-13 14:24

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0030_auto_20210413_1043'),
    ]

    operations = [
        migrations.CreateModel(
            name='Terms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Заголовок')),
                ('title_en', models.CharField(max_length=50, verbose_name='Title')),
                ('text', ckeditor.fields.RichTextField(max_length=30000, verbose_name='Описание')),
                ('text_en', ckeditor.fields.RichTextField(max_length=30000, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Термс',
                'verbose_name_plural': 'Emercoin and Conditions',
            },
        ),
        migrations.CreateModel(
            name='Privacy',
            fields=[
                ('terms_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='info.terms')),
            ],
            options={
                'verbose_name': 'Privacy Policy',
                'verbose_name_plural': 'Privacy Policy',
            },
            bases=('info.terms',),
        ),
    ]
