import hashlib

import requests

from emercoin.settings import MEDIA_URL, MEDIA_ROOT


def download(link):
    filename = link.split('/')[-1]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/41.0.2228.0'
                      ' Safari/537.36', }
    try:
        r = requests.get(link, headers=headers, timeout=4.0)
    except Exception:
        return None, None
    dw_hash = hashlib.sha256(r.content).hexdigest()
    print(dw_hash)
    try:
        f = open(f'{MEDIA_ROOT}/{filename}', 'br').read()
        file_hash = hashlib.sha256(f).hexdigest()
        if dw_hash == file_hash:
            return True, None
        else:
            filename = filename.replace('.', '_1.')
            open(f'{MEDIA_ROOT}/{filename}', 'wb').write(r.content)
            return True, filename
    except Exception as e:
        print(e)
        open(f'{MEDIA_ROOT}/{filename}', 'wb').write(r.content)
        return True, None


def auto_upload_images(text):
    """Найти все ссылки изображений в html, скачать и заменить ссылками
     на локальное хранилище /media/"""
    if not text:
        return text
    cur = 1
    while True:
        cur = text.find('src=', cur + 4)
        if cur == -1:
            break
        link_start = text.find('"', cur)
        link_finish = text.find('"', link_start + 1)
        link = text[link_start + 1:link_finish]
        if link.find('http') == -1:
            continue
        filename = link.split('/')[-1]
        print(cur, link, filename)
        result, new_name = download(link)
        if result:
            text = text.replace(
                link,
                f'{MEDIA_URL}{new_name if new_name else filename}', 1)
    return text
