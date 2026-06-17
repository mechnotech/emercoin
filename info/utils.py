import hashlib

import requests

from emercoin.settings import (
    MEDIA_URL,
    MEDIA_ROOT,
)


def download(link):
    filename = link.split('/')[-1]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/41.0.2228.0'
                      ' Safari/537.36', }
    try:
        r = requests.get(link, headers=headers, timeout=4.0)
    except IOError:
        return None, None
    dw_hash = hashlib.sha256(r.content).hexdigest()

    try:
        f = open(f'{MEDIA_ROOT}/{filename}', 'br').read()
        file_hash = hashlib.sha256(f).hexdigest()
        if dw_hash == file_hash:
            return True, None
        else:
            filename = filename.replace('.', '_1.')
            open(f'{MEDIA_ROOT}/{filename}', 'wb').write(r.content)
            return True, filename
    except (FileNotFoundError, FileExistsError):
        open(f'{MEDIA_ROOT}/{filename}', 'wb').write(r.content)
        return True, None


def image_check(filename):
    ending = filename.split('.')[-1]
    if ending == 'png' or ending == 'jpeg' or ending == 'jpg' \
            or ending == 'svg':
        return True
    return False


def auto_upload_images(text):
    """Найти все ссылки изображений в html, скачать и заменить ссылками
     на локальное хранилище /media/"""
    if not text:
        return text
    cur = 1
    while True:
        iframe = text.find('<iframe', cur)
        if iframe > -1:
            cur = text.find('</iframe', cur)
        cur = text.find('src=', cur + 4)
        if cur == -1:
            break
        link_start = text.find('"', cur)
        link_finish = text.find('"', link_start + 1)
        link = text[link_start + 1:link_finish]

        # if link.find('http') == -1 and link.find('storage') != -1:
        #     filename = link.split('/')[-1]
        #     if image_check(filename):
        #         new_link = 'https://emercoin.com' + link
        #         result, new_name = download(new_link)
        #         if result:
        #             text = text.replace(
        #                 link,
        #                 f'{MEDIA_URL}{new_name if new_name else filename}',
        #                 1)

        if link.find('http') == -1:
            continue
        filename = link.split('/')[-1]
        result, new_name = download(link)
        if result:
            text = text.replace(
                link,
                f'{MEDIA_URL}{new_name if new_name else filename}', 1)
    return text


def cut_self_href(text):
    if not text:
        return text
    return text.replace('href="https://emercoin.com', 'href="')


def cut_space(text):
    if not text:
        return text
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&#39;', "'")
    text = text.replace('&quot;', '"')
    return text


def get_blank_page(request):
    return 'blankpage_en.html'


def is_lang_rus(request):
    return False
