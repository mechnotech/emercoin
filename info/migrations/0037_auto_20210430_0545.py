# Generated by Django 3.1.7 on 2021-04-30 05:45

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0036_auto_20210415_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='<p>Этот раздел ещё не переведен на русский</p> <p>Вы поможете сообществу, если переведете его</p> <p>&nbsp;</p> <p><a class="button button-telegram" href="https://t.me/emernews" onclick="dataLayer.push({\'event\': \'telegram_community\'});" rel="nofollow" target="_blank">Telegram</a></p>', help_text='Текст (не более 15 тыс символов)', max_length=30000, null=True, verbose_name='Текст новости'),
        ),
        migrations.AlterField(
            model_name='news',
            name='text_en',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='<p>This section has not been translated yet.</p><p>You can help the community by translating this section into English</p><p><a class="button button-telegram" href="https://t.me/emerсoin_official" onclick="dataLayer.push({\'event\': \'telegram_community\'});" rel="nofollow" target="_blank">Telegram</a></p>', help_text='Post (no more than 15K letters)', max_length=30000, null=True, verbose_name='News text'),
        ),
    ]