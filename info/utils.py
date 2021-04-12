import hashlib

import requests
from django.core.mail import send_mail
from django.contrib import messages

from emercoin.settings import (
    MEDIA_URL,
    MEDIA_ROOT,
    EMAIL_HOST_USER,
    SUPPORT,
    GOOGLE_RECAPTCHA_SECRET_KEY
)


def check_recaptcha(function):
    def wrap(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.method == 'POST':
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post(
                'https://www.google.com/recaptcha/api/siteverify',
                data=data
            )
            result = r.json()
            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


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
    if isinstance(text, tuple):
        print(text)
    cur = 1
    while True:
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


def get_blank_page(request):
    if request.LANGUAGE_CODE == 'ru':
        return 'blankpage.html'
    else:
        return 'blankpage_en.html'


def is_lang_rus(request):
    if request.LANGUAGE_CODE == 'ru':
        return True
    return False


def send_support(form):
    name = str(form.cleaned_data.get('name'))
    email = str(form.cleaned_data.get('email'))
    message = str(form.cleaned_data.get('message'))
    send_mail(
        subject='С сайта emercoin',
        message=f'Пользователь {name} ( {email} ) написал:\n "{message}"',
        from_email=EMAIL_HOST_USER,
        recipient_list=(SUPPORT,),
        fail_silently=False,
    )
