# Generated by Django 3.1.7 on 2021-04-08 10:36

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emerdocs', '0003_auto_20210408_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docpage',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='<p>Этот раздел ещё не переведен на русский</p> <p>Вы поможете сообществу, если переведете его</p> <p>&nbsp;</p> <p><a class="button button-telegram" href="https://t.me/emernews" onclick="dataLayer.push({\'event\': \'telegram_community\'});" rel="nofollow" target="_blank">Telegram</a></p>', help_text='Текст (не более 200 тыс символов)', max_length=200000, verbose_name='Текст документа'),
        ),
        migrations.AlterField(
            model_name='docpage',
            name='text_en',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='<p>This section has not been translated yet.</p><p>You can help the community by translating this section into English</p><p><a class="button button-telegram" href="https://t.me/emerсoin_official" onclick="dataLayer.push({\'event\': \'telegram_community\'});" rel="nofollow" target="_blank">Telegram</a></p>', help_text='Text (no more 200K letters)', max_length=200000, verbose_name='Document text'),
        ),
    ]
