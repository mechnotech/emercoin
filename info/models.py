from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from colorfield.fields import ColorField
from django.core.validators import (
    FileExtensionValidator,
)
from django.core.validators import (
    URLValidator, MinValueValidator, MaxValueValidator
)
from django.db import models
from slugify import slugify

from emercoin.settings import BASE_DIR
from .utils import auto_upload_images, cut_self_href

with open(f'{BASE_DIR}/templates/help_us.html', 'r') as f:
    HELP_US = f.read()
with open(f'{BASE_DIR}/templates/help_us_en.html', 'r') as f:
    HELP_US_EN = f.read()


def desktop_image_validator(image):
    pass
    # h, w, size = 390, 1110, 5 * 1048576
    # errors = []
    # if image.height != h or image.width != w:
    #     errors.append(f'Размер картинки для мобильного должен быть {w}x{h}!')
    # if image.size > size:
    #     errors.append(f'Файл слишком большой (не более 1 Mб)')
    # if errors:
    #     raise ValidationError(errors)


def mobile_image_validator(image):
    pass
    # h, w, size = 350, 450, 1048576
    # errors = []
    # if image.height != h or image.width != w:
    #     errors.append(f'Размер картинки для десктопа должен быть {w}x{h}!')
    # if image.size > size:
    #     errors.append(f'Файл слишком большой (не более 5 Mб)')
    # if errors:
    #     raise ValidationError(errors)


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
    mobile_img_en = models.ImageField(
        'Mobile image',
        upload_to='info/',
        blank=True,
        null=True,
        max_length=150,
        help_text='If exists ~(450*350 pixel) no more 1Mb please)',

    )
    desktop_img_en = models.ImageField(
        'Desktop image',
        upload_to='info/',
        blank=True,
        null=True,
        max_length=150,
        help_text='If exists ~(1110*390 pixel, no more 5 Мб please)',

    )

    # def save(self, *args, **kwargs):
    #     if not self.mobile_img_en:
    #         self.mobile_img_en = self.mobile_img
    #     if not self.desktop_img_en:
    #         self.desktop_img_en = self.desktop_img
    #     super().save(*args, **kwargs)

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
    title_en = models.CharField('Title', max_length=20, blank=True, null=True)
    text = models.TextField('Описание', max_length=500, blank=False)
    text_en = models.TextField('Description', max_length=500, blank=True,
                               null=True)
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
    text = RichTextField('Краткое описание', max_length=1500, blank=False)
    text_en = RichTextField('Short description', max_length=1500, blank=True,
                            null=True)
    text_more = RichTextField(
        'Дополнительное описание',
        max_length=2000,
        blank=False)
    text_more_en = RichTextField(
        'Long description',
        max_length=2000,
        blank=True, null=True)
    scenarios = models.TextField(
        'Где применимо',
        help_text='Список тезисисов, разделитель  - |',
        max_length=1000,
        blank=False,
        default='Там | Тут'
    )
    scenarios_en = models.TextField(
        'Where can use',
        help_text='List of theses, divider  - |',
        max_length=1000,
        blank=True,
        null=True,
        default='Here | and Here'
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

    def best_for_en(self):
        return self.scenarios_en.split('|')

    def __str__(self):
        return self.title


class Content(models.Model):
    """Публикации СМИ о нас"""
    date = models.DateField('Дата публикаци', editable=True, )
    link = models.URLField('Ссылка на публикацию', max_length=200)
    brif = models.CharField('Заголовок публикации', max_length=80)

    class Meta:
        ordering = ['date']
        verbose_name_plural = 'Публикации СМИ'
        verbose_name = 'Публикация СМИ'

    def __str__(self):
        return self.brif


class Media(models.Model):
    """ СМИ """
    name = models.CharField('Название СМИ', blank=False, max_length=25)
    logo = models.FileField(
        'Логотип СМИ малый',
        upload_to='info/',
        blank=False,
        max_length=150,
        validators=[FileExtensionValidator(['jpg', 'png', 'svg'])],
        default=None)
    logo_big = models.FileField(
        'Большой логотип СМИ',
        upload_to='info/',
        blank=False,
        max_length=150,
        validators=[FileExtensionValidator(['jpg', 'png', 'svg'])],
        default=None,
        null=True)
    contents = models.ManyToManyField(
        Content,
        through='MediaContent',
        related_name='medium',
    )

    @property
    def count(self):
        return self.contents.count()

    def get_contents(self):
        content = []
        for i in self.mediacontent_set.all().order_by('-t_content__date'):
            content.append(i)
        return content

    class Meta:
        ordering = ['-pk']
        verbose_name_plural = 'СМИ'
        verbose_name = 'СМИ'

    def __str__(self):
        return self.name


class MediaContent(models.Model):
    t_media = models.ForeignKey(Media, on_delete=models.CASCADE)
    t_content = models.ForeignKey(Content, on_delete=models.CASCADE)

    def __str__(self):
        return f'Посты СМИ {self.t_media} - {self.t_content}'


class RoadMap(models.Model):
    """ Дорожная карта"""
    year = models.PositiveSmallIntegerField(
        'Год',
        default=2013,
        help_text='Год, например 2021',
        validators=[MinValueValidator(2012), MaxValueValidator(2100)]
    )
    text = RichTextField(
        'События',
        help_text='События или задачи года (каждое с новой строки)',
        max_length=1000
    )
    text_en = RichTextField(
        'Goals',
        help_text='Events and goals of year (with new paragraph for each)',
        max_length=1000,
        blank=True,
        null=True,
    )

    @property
    def short_text(self):
        textlist = self.text.split('</p>')
        return '</p>'.join(textlist[:2])

    @property
    def short_text_en(self):
        textlist = self.text_en.split('</p>')
        return '</p>'.join(textlist[:2])

    class Meta:
        ordering = ['year']
        verbose_name_plural = 'Дорожная карта'
        verbose_name = 'Год Дорожной карты'

    def __str__(self):
        return str(self.year)


class News(models.Model):
    """ Новости """
    title = models.CharField('Заголовок', max_length=150, blank=True,
                             null=True)
    title_en = models.CharField('Title', max_length=150, blank=True, null=True)
    slug = models.SlugField(
        'Slug',
        unique=True,
        allow_unicode=False,
        max_length=250,
        blank=True,
        help_text='Часть URL адреса новости, если не указывать явно -'
                  ' заполняется автоматически из Заголовка')
    date = models.DateTimeField('Дата и время', editable=True)
    image = models.ImageField(
        'Картинка новости',
        max_length=250,
        blank=True,
        null=True,
        help_text='Изображение 420*280 (примерно)'
    )
    image_en = models.ImageField(
        'News image',
        max_length=250,
        blank=True,
        null=True,
        help_text='Image ~ 420*280 px'
    )
    text = RichTextUploadingField(
        'Текст новости',
        max_length=30000,
        blank=True,
        null=True,
        help_text='Текст (не более 15 тыс символов)',
        default=HELP_US

    )
    text_en = RichTextUploadingField(
        'News text',
        max_length=30000,
        blank=True,
        null=True,
        help_text='Post (no more than 15K letters)',
        default=HELP_US_EN
    )

    def save(self, *args, **kwargs):
        self.text = auto_upload_images(self.text)
        self.text_en = auto_upload_images(self.text_en)
        self.text = cut_self_href(self.text)
        self.text_en = cut_self_href(self.text_en)

        if not self.slug:
            if self.title and not self.title_en:
                self.slug = slugify(self.title)
            elif self.title_en:
                self.slug = slugify(self.title_en)
            else:
                return
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Новости'
        verbose_name = 'Новость'

    def __str__(self):
        return f'Новость - {self.title}{self.title_en}'


class Person(models.Model):
    name = models.CharField('Имя', max_length=90, blank=False)
    name_en = models.CharField('Name', max_length=90, blank=True, null=True)
    image = models.ImageField(
        'Фото',
        max_length=250,
        blank=False,
        help_text='Изображение 360*360 квадрат (примерно)'
    )
    whois = models.CharField('Роль или должность', max_length=150, blank=False)
    whois_en = models.CharField('The role', max_length=150, blank=True,
                                null=True)
    info_short = RichTextField(
        'Краткое инфо',
        max_length=450,
        blank=False, help_text='Не более 250 символов')
    info_short_en = RichTextField(
        'Short_info',
        max_length=450,
        null=True,
        blank=True, help_text='No more 250 letters')
    info = RichTextField(
        'Полное инфо',
        max_length=1500,
        blank=True,
        help_text='Не более 550 символов')
    info_en = RichTextField(
        'Full info',
        max_length=1500,
        blank=True,
        null=True,
        help_text='No more 550 letters')
    is_team = models.BooleanField('Член команды?', default=False)
    is_adviser = models.BooleanField('Активист?', default=False)
    linkedin = models.URLField('LinkedIn', max_length=250, blank=True)
    facebook = models.URLField('Facebook', max_length=250, blank=True)
    twitter = models.URLField('Twitter', max_length=250, blank=True)

    # telegram = models.URLField('Telegram', max_length=250, blank=True)
    # github = models.URLField('Github', max_length=250, blank=True)

    @property
    def socials(self):
        return (self.linkedin,
                self.facebook, self.twitter)

    class Meta:
        ordering = ['pk']
        verbose_name_plural = 'Персоны'
        verbose_name = 'Персона'

    def __str__(self):
        return self.name


class Company(models.Model):
    title = models.CharField('Название', max_length=150, blank=False)
    slug = models.SlugField(
        'Slug',
        unique=True,
        allow_unicode=False,
        max_length=250,
        blank=True,
        help_text='Часть URL адреса новости, если не указывать явно -'
                  ' заполняется автоматически из Названия')
    logo = models.FileField(
        'Логотип Компании малый',
        upload_to='info/',
        blank=False,
        max_length=150,
        validators=[FileExtensionValidator(['jpg', 'png', 'svg'])],
        default=None,
        help_text='Размер 100*40 пикселей'
    )
    logo_big = models.FileField(
        'Большой логотип Компании',
        upload_to='info/',
        blank=False,
        max_length=150,
        validators=[FileExtensionValidator(['jpg', 'png', 'svg'])],
        default=None,
        null=True,
        help_text='Размер 200*80 пикселей'
    )
    is_partner = models.BooleanField(
        'Партнер?',
        default=True,
        help_text='Заключили партнерство?'
    )
    is_used = models.BooleanField(
        'Применяют?',
        default=False,
        help_text='Применяют технологии?'
    )
    text = RichTextField('Краткое описание', max_length=1500, blank=False)
    text_en = RichTextField('Short description', max_length=1500,
                            blank=True, null=True)
    text_more = RichTextField(
        'Дополнительное описание',
        max_length=2000,
        blank=False)
    text_more_en = RichTextField(
        'More description',
        max_length=2000,
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Компании'
        verbose_name = 'Компания'

    def __str__(self):
        return self.title


class Terms(models.Model):
    title = models.CharField('Заголовок', max_length=50)
    title_en = models.CharField('Title', max_length=50)
    date = models.DateTimeField('Дата и время', editable=True)
    text = RichTextField('Описание', max_length=50000, blank=False)
    text_en = RichTextField('Description', max_length=50000, blank=False)

    class Meta:
        verbose_name_plural = 'Emercoin and Conditions'
        verbose_name = 'Термс'

    def __str__(self):
        return self.title


class Privacy(models.Model):
    title = models.CharField('Заголовок', max_length=50)
    title_en = models.CharField('Title', max_length=50)
    date = models.DateTimeField('Дата и время', editable=True)
    text = RichTextField('Описание', max_length=50000, blank=False)
    text_en = RichTextField('Description', max_length=50000, blank=False)

    class Meta:
        verbose_name_plural = 'Privacy Policy'
        verbose_name = 'Privacy Policy'

    def __str__(self):
        return self.title
