"""
Замораживает динамический Django-сайт в статический HTML в каталоге dist/.

Использует django.test.Client для рендера каждого URL существующими шаблонами,
раскладывает результат как <path>/index.html (nginx: try_files $uri $uri/index.html).
Копирует публичную статику (info/static -> dist/static) и медиа (media -> dist/media).

Запуск:  python manage.py freeze
"""
import math
import re
import shutil
from pathlib import Path

from django.core.management.base import BaseCommand
from django.test import Client
from django.urls import get_resolver, reverse
from django.urls.resolvers import URLPattern, URLResolver

from emercoin.settings import BASE_DIR, MEDIA_URL
from info.models import News, Services, Company
from info.views import DEFAULT_PAGE_SIZE

DIST = Path(BASE_DIR) / 'dist'
SRC_STATIC = Path(BASE_DIR) / 'info' / 'static'
SRC_MEDIA = Path(BASE_DIR) / 'media'
# Если MEDIA_URL абсолютный (R2/CDN) — медиа не кладём в dist, а ссылки
# /media/... переписываем на внешний хост.
EXTERNAL_MEDIA = MEDIA_URL.startswith('http')

# URL-имена, которые не нужно замораживать (служебные).
SKIP_PREFIXES = ('/admin', '/ckeditor', '/i18n')

NEWS_PAGINATION_RE = re.compile(r'href="/news/?\?page=(\d+)"')
# Старый i18n-контент в БД содержит абсолютные ссылки с языковым префиксом:
# /en/foo -> /foo, /en -> /, /en#x -> /#x (то же для /ru).
LANG_DIR_RE = re.compile(r'(href|src)="/(?:en|ru)/')
LANG_BARE_RE = re.compile(r'(href|src)="/(?:en|ru)(?=["#])')
# HTML-комментарии (остатки ru-вёрстки) — вырезаем (не трогаем <!DOCTYPE>).
HTML_COMMENT_RE = re.compile(r'<!--.*?-->', re.DOTALL)
# Кириллические буквы-двойники латиницы (гомоглифы).
HOMOGLYPHS = {
    'А': 'A', 'В': 'B', 'Е': 'E', 'К': 'K', 'М': 'M', 'Н': 'H', 'О': 'O',
    'Р': 'P', 'С': 'C', 'Т': 'T', 'Х': 'X', 'а': 'a', 'е': 'e', 'о': 'o',
    'р': 'p', 'с': 'c', 'х': 'x', 'у': 'y', 'і': 'i', 'ј': 'j', 'ѕ': 's',
    'І': 'I', 'Ј': 'J', 'Ѕ': 'S',
}


def fix_homoglyphs(s):
    """Заменяет кириллический двойник на латиницу только если рядом латиница
    (т.е. это слово на латинице с одной подменённой буквой). Настоящий русский
    текст (соседи-кириллица) не трогаем."""
    chars = list(s)
    n = len(chars)
    for i, ch in enumerate(chars):
        rep = HOMOGLYPHS.get(ch)
        if not rep:
            continue
        prev = chars[i - 1] if i > 0 else ''
        nxt = chars[i + 1] if i + 1 < n else ''
        if (prev.isascii() and prev.isalnum()) or (nxt.isascii() and nxt.isalnum()):
            chars[i] = rep
    return ''.join(chars)


def rewrite_html(html):
    """Чистка готового HTML: ссылки, пагинация, ru-комментарии, гомоглифы."""
    html = LANG_DIR_RE.sub(r'\1="/', html)
    html = LANG_BARE_RE.sub(r'\1="/', html)
    if EXTERNAL_MEDIA:
        html = html.replace('/media/', MEDIA_URL)
    html = HTML_COMMENT_RE.sub('', html)
    html = fix_homoglyphs(html)

    def repl(m):
        n = int(m.group(1))
        return 'href="/news/"' if n == 1 else f'href="/news/page/{n}/"'
    return NEWS_PAGINATION_RE.sub(repl, html)


class Command(BaseCommand):
    help = 'Build a static snapshot of the site into dist/'

    def handle(self, *args, **options):
        self.client = Client()
        self.ok = 0
        self.bad = 0

        self._reset_dist()
        self._copy_assets()
        self._freeze_named_urls()
        self._freeze_db_objects()
        self._freeze_specials()
        self._freeze_news_pagination()
        self._freeze_404()

        self.stdout.write(self.style.SUCCESS(
            f'\nDone. pages OK={self.ok}, problems={self.bad}, out={DIST}'))

    # ---------- infrastructure ----------
    def _reset_dist(self):
        if DIST.exists():
            shutil.rmtree(DIST)
        DIST.mkdir(parents=True)

    def _copy_assets(self):
        shutil.copytree(SRC_STATIC, DIST / 'static')
        self.stdout.write('copied static/')
        if EXTERNAL_MEDIA:
            self.stdout.write(f'media external ({MEDIA_URL}) — not bundled')
        elif SRC_MEDIA.exists():
            shutil.copytree(SRC_MEDIA, DIST / 'media')
            self.stdout.write('copied media/')

    # ---------- url discovery ----------
    def _named_zero_arg_urls(self):
        names = set()

        def walk(patterns):
            for p in patterns:
                if isinstance(p, URLResolver):
                    walk(p.url_patterns)
                elif isinstance(p, URLPattern):
                    if p.name and p.pattern.regex.groups == 0:
                        names.add(p.name)
        walk(get_resolver().url_patterns)

        urls = set()
        for name in names:
            try:
                url = reverse(name)
            except Exception:
                continue
            if url.startswith(SKIP_PREFIXES):
                continue
            urls.add(url)
        return urls

    # ---------- freezing ----------
    def _freeze_named_urls(self):
        for url in sorted(self._named_zero_arg_urls()):
            self._save(url)

    def _freeze_db_objects(self):
        for s in Services.objects.all():
            self._save(f'/{s.slug}/')
        for c in Company.objects.all():
            self._save(f'/partners-and-projects/{c.slug}')
        for n in News.objects.filter(title_en__isnull=False):
            self._save(f'/news/{n.slug}/')

    def _freeze_specials(self):
        # реальные файлы с расширением
        self._save('/robots.txt', as_file=True)
        self._save('/sitemap.xml', as_file=True)
        # RSS: кладём как feed/index.html (xml-содержимое)
        self._save('/feed')

    def _freeze_news_pagination(self):
        count = News.objects.filter(title_en__isnull=False).count()
        pages = max(1, math.ceil(count / DEFAULT_PAGE_SIZE))
        for p in range(1, pages + 1):
            r = self.client.get('/news', {'page': p}, follow=True)
            if r.status_code != 200:
                self.bad += 1
                self.stdout.write(self.style.WARNING(
                    f'  news page {p}: HTTP {r.status_code}'))
                continue
            html = rewrite_html(r.content.decode('utf-8'))
            target = (DIST / 'news' / 'index.html') if p == 1 else \
                (DIST / 'news' / 'page' / str(p) / 'index.html')
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(html, encoding='utf-8')
            self.ok += 1

    def _freeze_404(self):
        r = self.client.get('/this-page-does-not-exist-404/')
        (DIST / '404.html').write_bytes(r.content)
        self.stdout.write('wrote 404.html')

    def _save(self, url, as_file=False):
        r = self.client.get(url, follow=True)
        if r.status_code != 200:
            self.bad += 1
            self.stdout.write(self.style.WARNING(
                f'  {url}: HTTP {r.status_code}'))
            return
        body = r.content
        if 'text/html' in r.get('Content-Type', ''):
            body = rewrite_html(r.content.decode('utf-8')).encode('utf-8')

        if as_file:
            target = DIST / url.lstrip('/')
        elif url == '/':
            target = DIST / 'index.html'
        else:
            target = DIST / url.strip('/') / 'index.html'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(body)
        self.ok += 1
