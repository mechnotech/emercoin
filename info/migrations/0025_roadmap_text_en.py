# Generated by Django 3.1.7 on 2021-03-30 12:35

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0024_auto_20210330_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='roadmap',
            name='text_en',
            field=ckeditor.fields.RichTextField(blank=True, help_text='Events and goals of year (with new paragraph for each)', max_length=1000, null=True, verbose_name='Goals'),
        ),
    ]
