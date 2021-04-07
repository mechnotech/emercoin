# Generated by Django 3.1.7 on 2021-03-23 12:48

import ckeditor.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0011_auto_20210323_1154'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoadMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveSmallIntegerField(default=2013, help_text='Год, например 2021', validators=[django.core.validators.MinValueValidator(2012), django.core.validators.MaxValueValidator(2100)], verbose_name='Год')),
                ('text', ckeditor.fields.RichTextField(help_text='События или задачи года (каждое с новой строки)', max_length=1000, verbose_name='События')),
            ],
        ),
    ]
