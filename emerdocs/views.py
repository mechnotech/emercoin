from django.shortcuts import render, redirect, get_object_or_404

from emercoin.settings import MENU
from .models import DocPage


def recursive(menu, url, flag=False):
    for item in menu:
        if item.get('url') == url:
            item['active'] = True
            return menu, True
        if item.get('toggle'):
            _, flag = recursive(item['toggle'], url)
            if flag:
                item['active'] = True
    return menu, flag


def activate(url):
    menu = MENU
    return recursive(menu, url)[0]


def render_docs(request):
    url = request.resolver_match.url_name
    menu = activate(url)
    # page = get_object_or_404(DocPage, url=url)
    page = get_object_or_404(DocPage, pk=1)
    context = {
        'menu': menu,
        'page_data': page,
    }
    if request.LANGUAGE_CODE == 'ru':
        return render(request, 'page.html', context)
    else:
        return render(request, 'page_en.html', context)


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