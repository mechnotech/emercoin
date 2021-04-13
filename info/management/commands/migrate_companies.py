import pathlib
import sqlite3

from django.core.management.base import BaseCommand

from info.models import Company
from info.utils import download

db = pathlib.Path('oldemer.db').absolute()
conn = sqlite3.connect(db)


def post_ru(post):
    title = post[1]
    text = post[11]
    text_more = post[12]
    slug = post[2]
    try:
        pt = Company.objects.get(slug=slug)
    except Exception:
        pt = None

    if pt:
        pt.title = str(title)
        pt.text = str(text)
        pt.text_more = str(text_more)
        pt.save()
    else:
        Company.objects.get_or_create(
            slug=slug,
            title=title,
            text=text,
            text_more=text_more,
        )


def post_en(post):
    title = post[1]
    text = post[11]
    text_more = post[12]
    image_lit = post[8]
    image_big = post[9]
    if not image_big:
        image_big = image_lit
    _, logo_lit = download(f'https://emercoin.com/{image_lit}')
    if not logo_lit:
        logo_lit = image_lit.split('/')[-1]
    _, logo_big = download(f'https://emercoin.com/{image_big}')
    if not logo_big:
        logo_big = image_big.split('/')[-1]
    slug = post[2]
    is_using = post[-1]
    try:
        pt = Company.objects.get(slug=slug)
    except Exception:
        pt = None

    if pt:
        pt.title = str(title)
        pt.text_en = str(text)
        pt.text_more_en = str(text_more)
        pt.logo = logo_lit
        pt.logo_big = logo_big
        pt.is_used = True if is_using else False
        pt.is_partner = False if is_using else True
        pt.save()
    else:
        Company.objects.get_or_create(
            slug=slug,
            title=title,
            text_en=text,
            text_more_en=text_more,
            logo=logo_lit,
            logo_big=logo_big,
            is_used=True if is_using else False,
            is_partner=False if is_using else True
        )


class Command(BaseCommand):
    help = 'Переместить старые компании'

    def handle(self, *args, **options):
        current = Company.objects.count()
        c = conn.cursor()
        c.execute(
            "SELECT * FROM companies WHERE lang='en' OR lang='ru'"
        )
        for p in c.fetchall():
            if p[4] == 'en':
                post_en(p)
            if p[4] == 'ru':
                post_ru(p)

        result = Company.objects.count() - current
        print(f'В базу добавлено {result} компаний')
