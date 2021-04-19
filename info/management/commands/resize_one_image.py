import os
import pathlib

from PIL import Image
from django.core.management.base import BaseCommand
from resizeimage import resizeimage


def resize_me(source, destination, width):

    imgf = pathlib.Path(source).absolute()
    sz = os.path.getsize(imgf)
    with open(imgf, 'r+b') as f:
        with Image.open(f) as image:
            cover = resizeimage.resize_width(image, width)
            cover.save(destination, image.format)
    return sz


class Command(BaseCommand):
    help = 'Ужать одну картинку'

    def handle(self, *args, **options):
        source = 'media-full/postmet.png'
        destination = 'media-resized/postmet_mid.png'
        width = 600

        sz = resize_me(source, destination, width)

        print(f'Ок, {sz}')
