import datetime
import pathlib
import sqlite3

from django.core.management.base import BaseCommand

from info.models import News

db = pathlib.Path('oldemer.db').absolute()
conn = sqlite3.connect(db)


def post_ru(post):
    title = post[1]
    text = post[11]
    image = post[9].split('/')[-1]
    slug = post[2]
    # '2018-10-23 18:33:00'
    date_field = post[-2]
    date = datetime.datetime.strptime(date_field, '%Y-%m-%d %H:%M:%S')
    try:
        pt = News.objects.get(slug=slug)
    except Exception:
        pt = None
    if pt:
        pt.title = str(title)
        pt.text = str(text)
        pt.date = date
        pt.image = image
        pt.save()
    else:
        News.objects.get_or_create(
            slug=slug,
            title=str(title),
            text=str(text),
            image=image,
            date=date,
        )


def post_en(post):
    title = post[1]
    text = post[11]
    image = post[9].split('/')[-1]
    slug = post[2]
    # '2018-10-23 18:33:00'
    date_field = post[-2]
    date = datetime.datetime.strptime(date_field, '%Y-%m-%d %H:%M:%S')
    try:
        pt = News.objects.get(slug=slug)
    except Exception:
        pt = None
    print(title, date, slug, image)
    if pt:
        pt.title_en = str(title)
        pt.text_en = str(text)
        pt.date = date
        pt.image_en = image
        pt.save()
    else:
        News.objects.get_or_create(
            slug=slug,
            title_en=title,
            text_en=text,
            image_en=image,
            date=date,
        )


class Command(BaseCommand):
    help = 'Переместить старые новости'

    def handle(self, *args, **options):
        current = News.objects.count()
        c = conn.cursor()
        c.execute(
            "SELECT * FROM posts WHERE status=1 AND"
            " ( lang='en' OR lang='ru')")
        for p in c.fetchall():
            if p[4] == 'en':
                post_en(p)
            if p[4] == 'ru':
                post_ru(p)

        result = News.objects.count() - current
        print(f'В базу добавлено {result} старых постов')
