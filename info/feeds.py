from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import News
import html2text


class MyFeed(Feed):

    def __init__(self):
        self.language = None
        self.title = 'Emercoin News'
        self.link = '/en/news'
        self.description = 'Last 5 news about Emercoin'

    def get_object(self, request, *args, **kwargs):
        if request.LANGUAGE_CODE == 'ru':
            self.language = 'ru'
            self.title = 'Новости Эмеркоин'
            self.link = '/ru/news'
            self.description = 'Пять последних новостей об Эмеркоине'
        else:
            self.language = 'en'
            self.title = 'Emercoin News'
            self.link = '/en/news'
            self.description = 'Last 5 news about Emercoin'

    def items(self):
        if self.language == 'ru':
            return News.objects.filter(
                title__isnull=False).order_by('-date')[:5]
        else:
            return News.objects.filter(
                title_en__isnull=False).order_by("-date")[:5]

    def item_title(self, item):
        if self.language == 'ru':
            return item.title
        else:
            return item.title_en

    def item_description(self, item):
        if self.language == 'ru':
            return truncatewords(html2text.html2text(item.text), 100)
        else:
            return truncatewords(html2text.html2text(item.text_en), 100)

    def item_link(self, item):
        if self.language == 'ru':
            return f'/ru/{item.slug}'
        else:
            return f'/en/{item.slug}'
