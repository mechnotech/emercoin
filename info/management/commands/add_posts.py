
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from info.models import News
import random
import datetime


images = ['chto-delat.png', '670ce7133c778048e50b48217f04fbe5.jpg',
          'ssl-sert-livecoin.jpg']


def get_rand_post():
    title = get_random_string(length=random.randint(10, 32),
                              allowed_chars='АкденсрВ')
    text = get_random_string(length=random.randint(100, 500),
                             allowed_chars='АИБГкдджзикенсрВ')
    print(title, type(title))
    print(str(title))
    News.objects.get_or_create(
        title=str(title),
        text=str(text),
        date=datetime.datetime.today(),
        image=random.choice(images)
    )


def get_rand_post_en():
    title = get_random_string(length=random.randint(10, 32),
                              allowed_chars='FSRghonwqz')
    text = get_random_string(length=random.randint(100, 500),
                             allowed_chars='FGVXSRgheuylonwqz')
    print(title, type(title))
    print(str(title))
    News.objects.get_or_create(
        title_en=str(title),
        text_en=str(text),
        date=datetime.datetime.today(),
        image_en=random.choice(images)
    )


class Command(BaseCommand):
    help = 'Добавить 50 рандомных постов в базу'

    def handle(self, *args, **options):
        current = News.objects.count()
        for _ in range(50):
            c = random.randint(0, 1)
            if c == 1:
                get_rand_post()
            else:
                get_rand_post_en()

        result = News.objects.count() - current
        print(f'В базу добавлено {result} рандомных постов')

