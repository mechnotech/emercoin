from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from info.utils import auto_upload_images


class DocPage(models.Model):
    url = models.SlugField(
        'Slug - URL',
        unique=True,
        allow_unicode=False,
        max_length=250,
        blank=False,
        help_text='Часть URL адреса документа, '
                  'по которому можно найти модель. Например "about-emercoin"'
    )
    text = RichTextUploadingField(
        'Текст документа',
        max_length=25000,
        blank=True,
        help_text='Текст (не более 25 тыс символов)'
    )
    text_en = RichTextUploadingField(
        'Document text',
        max_length=25000,
        blank=True,
        help_text='Text (no more 25K letters)'
    )

    def save(self, *args, **kwargs):
        self.text = auto_upload_images(self.text)
        self.text_en = auto_upload_images(self.text_en)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-pk']
        verbose_name_plural = 'Документация'
        verbose_name = 'Документ'

    def __str__(self):
        return f'Документ - {self.url}'