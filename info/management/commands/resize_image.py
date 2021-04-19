import os
import pathlib
import shutil

from django.core.management.base import BaseCommand
from PIL import Image
from resizeimage import resizeimage
from info.models import News


def post_en(post):
    post_image = post.image
    if not post_image:
        post_image = post.image_en
    print(post_image)
    imgf = pathlib.Path(f'media/{post_image}').absolute()
    dst = 'media-full/'
    shutil.copy(imgf, dst)
    sz = os.path.getsize(imgf)
    with open(imgf, 'r+b') as f:
        with Image.open(f) as image:
            cover = resizeimage.resize_width(image, 350)
            cover.save(f'media-resized/{post_image}', image.format)
    return sz


class Command(BaseCommand):
    help = 'Ужать большие файлы'

    def handle(self, *args, **options):
        result = 0
        common_sz = 0
        posts = News.objects.all()

        for p in posts:
            common_sz += post_en(p)
            result += 1

        print(f'В базе обновлено {result} старых изображений')
        print(f'Вес всех файлов {common_sz}')
