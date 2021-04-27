from copy import deepcopy

from django.contrib.postgres.search import SearchVector
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import requires_csrf_token

from emercoin.settings import MENU, P_CACHE
from .forms import SearchForm
from .models import DocPage
from django.views.decorators.gzip import gzip_page


def get_doc_blank_page(request):
    if request.LANGUAGE_CODE == 'ru':
        return 'blank_docs_page.html'
    else:
        return 'blank_docs_page_en.html'


def is_lang_rus(request):
    if request.LANGUAGE_CODE == 'ru':
        return True
    return False


def recursive(menu, url, flag=False):
    for item in menu:

        if item.get('url') == url:
            item['active'] = True
            return menu, True
        if item.get('toggle'):
            _, flag = recursive(item['toggle'], url)
            if flag:
                item['active'] = flag
                return menu, flag

    return menu, flag


def activate(url):
    menu = deepcopy(MENU)
    return recursive(menu, url)[0]


@cache_page(P_CACHE)
@gzip_page
def render_docs(request):
    form = SearchForm()
    url = request.resolver_match.url_name
    blank_page = get_doc_blank_page(request)
    menu = activate(url)
    page = get_object_or_404(DocPage, url=url)
    context = {
        'menu': menu,
        'form': form,
        'page_data': page,
        'blank': blank_page,
        'is_ru': is_lang_rus(request)
    }

    return render(request, 'page_en.html', context)


def search(text):
    res = DocPage.objects.annotate(
        search=SearchVector('text_en', 'text'), ).filter(search=text)
    urls = []
    for u in res:
        urls.append(u.url)
    return urls


@cache_page(P_CACHE)
@requires_csrf_token
def results(request):
    url = ''
    form = SearchForm()
    blank_page = get_doc_blank_page(request)
    menu = activate(url)
    context = {
        'menu': menu,
        'form': form,
        'sent': False,
        'blank': blank_page,
        'is_ru': is_lang_rus(request),
        # 'captcha_id': GOOGLE_RECAPTCHA_ID
    }
    if request.method == 'POST':
        form = SearchForm(request.POST)
        # if request.recaptcha_is_valid:
        if form.is_valid():
            context['page_data'] = search(form.cleaned_data['find'])
            context['sent'] = True
            return render(request, 'results.html', context)
        context['form'] = form

    if request.GET.get('sent'):
        context['sent'] = True
    return render(request, 'results.html', context)


def about_emercoin(request):
    return render_docs(request)


def about_redirect(request):
    return redirect('about-emercoin/')


def intro_currency(request):
    return render_docs(request)


def specifications(request):
    return render_docs(request)


def gui_wallet(request):
    return render_docs(request)


def cli_deamon(request):
    return render_docs(request)


def emer_api(request):
    return render_docs(request)


def press_kit(request):
    return render_docs(request)


def links(request):
    return render_docs(request)


def emerweb(request):
    return render_docs(request)


def other_wallets(request):
    return render_docs(request)


def trasted(request):
    return render_docs(request)


def linux_qs(request):
    return render_docs(request)


def command_line(request):
    return render_docs(request)


def emercoin_conf(request):
    return render_docs(request)


def ports(request):
    return render_docs(request)


def testnet(request):
    return render_docs(request)


def intro_services(request):
    return render_docs(request)


def emernvs(request):
    return render_docs(request)


def emerssh(request):
    return render_docs(request)


def emerssl_intro(request):
    return render_docs(request)


def emerssl_guide(request):
    return render_docs(request)


def emerssl_infocard(request):
    return render_docs(request)


def emerdns_intro(request):
    return render_docs(request)


def emerdpo_into(request):
    return render_docs(request)


def antifake(request):
    return render_docs(request)


def sn_publ(request):
    return render_docs(request)


def emermagnet(request):
    return render_docs(request)


def enumer(request):
    return render_docs(request)


def stake(request):
    return render_docs(request)


def work(request):
    return render_docs(request)


def secutity(request):
    return render_docs(request)


def docker(request):
    return render_docs(request)


def file_validator(request):
    return render_docs(request)


def randpay(request):
    return render_docs(request)


def recover(request):
    return render_docs(request)
