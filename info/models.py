from colorfield.fields import ColorField
from django.core.exceptions import ValidationError
from django.core.validators import (
    URLValidator
)
from django.core.validators import (
    get_available_image_extensions,
    FileExtensionValidator,
)
from django.db import models


def desktop_image_validator(image):
    h, w, size = 390, 1110, 5 * 1048576
    errors = []
    if image.height != h or image.width != w:
        errors.append(f'Размер картинки для мобильного должен быть {w}x{h}!')
    if image.size > size:
        errors.append(f'Файл слишком большой (не более 1 Mб)')
    if errors:
        raise ValidationError(errors)


def mobile_image_validator(image):
    h, w, size = 350, 450, 1048576
    errors = []
    if image.height != h or image.width != w:
        errors.append(f'Размер картинки для десктопа должен быть {w}x{h}!')
    if image.size > size:
        errors.append(f'Файл слишком большой (не более 5 Mб)')
    if errors:
        raise ValidationError(errors)


class Promo(models.Model):
    """
    Слайды Большого слайдера на главной странице
    """
    link = models.URLField(
        'Ссылка c Промо на новость (Главный слайдер)',
        max_length=200,
        unique=True,
        help_text='URL (не более 200 символов)',
        validators=[URLValidator]
    )
    bg_color = ColorField('Цвет фона полдожки', default='#FF0000')

    mobile_img = models.ImageField(
        'Картинка для мобильного',
        upload_to='info/',
        blank=False,
        max_length=150,
        help_text='Картинка для мобильного (450*350 пиксел) не больше 1Mb)',
        validators=[mobile_image_validator]
    )
    desktop_img = models.ImageField(
        'Картинка для десктопа',
        upload_to='info/',
        blank=False,
        max_length=150,
        help_text='Картинка для десктопа (1110*390 пиксел, не больше 5 Мб)',
        validators=[desktop_image_validator]
    )

    class Meta:
        ordering = ['-pk']
        verbose_name_plural = 'Промо слайды'
        verbose_name = 'Промо слайд'

    def __str__(self):
        return f'Промо слайд {self.pk}'


class AboutEmer(models.Model):
    """
    Блоки технологий для "О Блокчейне Эмера"
    """
    title = models.CharField('Заголовок', max_length=20, blank=False)
    text = models.TextField('Описание', max_length=500, blank=False)
    image = models.FileField(
        'Изображение блока',
        upload_to='info/',
        blank=False,
        max_length=150,
        validators=[FileExtensionValidator(['jpg', 'png', 'svg'])]
    )

    class Meta:
        ordering = ['-pk']
        verbose_name_plural = 'Блоки о блокчейне'
        verbose_name = 'Блок о блокчейне'

    def __str__(self):
        return self.title


class Services(models.Model):
    """
    Сервисы Эмера, такие как EmerDNS, EmerDPO и др.
    """
    title = models.CharField('Название', max_length=15, blank=False)
    slug = models.SlugField(
        'Slug',
        blank=False,
        help_text='Часть URL пути, например emerdns')
    text = models.TextField('Краткое описание', max_length=1500, blank=False)
    text_more = models.TextField(
        'Дополнительное описание',
        max_length=2000,
        blank=False)
    scenarios = models.TextField(
        'Где применимо',
        help_text='Список тезисисов, разделитель  - |',
        max_length=1000,
        blank=False,
        default='Там | Тут'
    )
    image = models.FileField(
        'Изображение блока (большое)',
        upload_to='info/',
        blank=False,
        max_length=150,
        validators=[FileExtensionValidator(['jpg', 'png', 'svg'])]
    )
    icon = models.FileField(
        'Иконка блока',
        upload_to='info/',
        blank=False,
        max_length=150,
        validators=[FileExtensionValidator(['jpg', 'png', 'svg'])],
        default=None
    )

    class Meta:
        ordering = ['pk']
        verbose_name_plural = 'Сервисы Эмера'
        verbose_name = 'Сервис Эмера'

    def best_for(self):
        return self.scenarios.split('|')

    def __str__(self):
        return self.title
