import pathlib
import sqlite3

from django.core.management.base import BaseCommand

from info.models import Media
from info.utils import download

db = pathlib.Path('oldemer.db').absolute()
conn = sqlite3.connect(db)


def post_en(post):
    name = post[1]
    image_lit = post[2]
    image_big = post[3]

    _, logo_lit = download(f'https://emercoin.com/{image_lit}')
    if not logo_lit:
        logo_lit = image_lit.split('/')[-1]
    _, logo_big = download(f'https://emercoin.com/{image_big}')
    if not logo_big:
        logo_big = image_big.split('/')[-1]

    Media.objects.get_or_create(
            name=name,
            logo=logo_lit,
            logo_big=logo_big,
        )


class Command(BaseCommand):
    help = 'Переместить старые Медиа'

    def handle(self, *args, **options):
        current = Media.objects.count()
        c = conn.cursor()
        c.execute(
            "SELECT * FROM presses"
        )
        for p in c.fetchall():
            post_en(p)

        result = Media.objects.count() - current
        print(f'В базу добавлено {result} Медиа')
