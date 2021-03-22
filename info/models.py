from django.core.exceptions import ValidationError
from django.core.validators import (
    MinValueValidator, MaxValueValidator,
    URLValidator, BaseValidator
)
from django.db import models
from colorfield.fields import ColorField


# class ImageSizeValidator(BaseValidator):
#     def __init__(self, limit_value):
#         super().__init__(limit_value)
#         self.is_desktop = is_desktop
#         self.errors = []
#         if is_desktop:
#             self.height, self.width, self.size = 390, 1110, 5 * 1048576
#         else:
#             self.height, self.width, self.size = 350, 450, 1048576
#
#     def __call__(self, value):
#         device = 'десктоп' if self.is_desktop else 'мобильного'
#         if object.height != self.height or object.width != self.width:
#             self.errors.append(
#                 f'Проверьте размеры изображения для {device}'
#                 f' ({self.height}*{self.width})')
#         if object.size > self.size:
#             self.errors.append(f'Изображение для {device} '
#                                f'не больше {self.size}')

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
