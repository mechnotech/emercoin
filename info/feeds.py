from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import News
import html2text


class MyFeed(Feed):
    title = 'Emercoin News'
    link = '/news'
    description = 'Last 5 news about Emercoin'

    def items(self):
        return News.objects.filter(
            title_en__isnull=False).order_by("-date")[:5]

    def item_title(self, item):
        return item.title_en

    def item_description(self, item):
        return truncatewords(html2text.html2text(item.text_en), 100)

    def item_link(self, item):
        return f'/news/{item.slug}'
