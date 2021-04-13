import pathlib
import sqlite3

from django.core.management.base import BaseCommand

from info.models import Content
from info.utils import download

db = pathlib.Path('oldemer.db').absolute()
conn = sqlite3.connect(db)


def post_en(post):
    brif = post[1]
    url = post[2]
    date = post[-1]

    Content.objects.get_or_create(
            brif=brif,
            link=url,
            date=date,
        )


class Command(BaseCommand):
    help = 'Переместить старые Медиа'

    def handle(self, *args, **options):
        current = Content.objects.count()
        c = conn.cursor()
        c.execute(
            "SELECT * FROM publications"
        )
        for p in c.fetchall():
            post_en(p)

        result = Content.objects.count() - current
        print(f'В базу добавлено {result} Медиа')
