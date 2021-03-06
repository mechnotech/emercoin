# Generated by Django 3.1.7 on 2021-03-25 06:59

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0014_auto_20210324_1321'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=90, verbose_name='Имя')),
                ('image', models.ImageField(help_text='Изображение 360*360 квадрат (примерно)', max_length=250, upload_to='', verbose_name='Фото')),
                ('whois', models.CharField(max_length=150, verbose_name='Роль или должность')),
                ('info_short', ckeditor.fields.RichTextField(help_text='Не более 250 символов', max_length=250, verbose_name='Краткое инфо')),
                ('info', ckeditor.fields.RichTextField(help_text='Не более 550 символов', max_length=550, verbose_name='Полное инфо')),
                ('is_team', models.BooleanField(default=False, verbose_name='Член команды?')),
                ('is_adviser', models.BooleanField(default=False, verbose_name='Адвайзер?')),
                ('linkedin', models.URLField(max_length=250, verbose_name='LinkedIn')),
                ('facebook', models.URLField(max_length=250, verbose_name='Facebook')),
                ('twitter', models.URLField(max_length=250, verbose_name='Twitter')),
                ('telegram', models.URLField(max_length=250, verbose_name='Twitter')),
                ('github', models.URLField(max_length=250, verbose_name='Twitter')),
            ],
            options={
                'verbose_name': 'Персона',
                'verbose_name_plural': 'Персоны',
            },
        ),
    ]
