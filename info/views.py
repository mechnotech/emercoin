from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import requires_csrf_token

from emercoin.settings import GOOGLE_RECAPTCHA_ID
from .forms import ContactForm
from .models import (
    Promo, AboutEmer, Services, Media, RoadMap, News, Person, Company,
    Terms, Privacy
)
from .utils import get_blank_page, is_lang_rus, send_support
from django.views.decorators.gzip import gzip_page

DEFAULT_PAGE_SIZE = 18


def get_paginated_view(request, recipe_list, page_size=DEFAULT_PAGE_SIZE):
    paginator = Paginator(recipe_list, page_size)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page, paginator


@gzip_page
def index(request):
    promos = Promo.objects.all()[:10]
    emer_blocks = AboutEmer.objects.all()
    services = Services.objects.all()
    medium = Media.objects.all()
    roadmap = RoadMap.objects.all()
    news = News.objects.order_by("-date")[:3]
    # advisers = Person.objects.filter(is_adviser=True)
    teammates = Person.objects.filter(is_team=True)[:4]
    context = {'promos': promos,
               'emer_blocks': emer_blocks,
               'services': services,
               'medium': medium,
               'roadmap': roadmap,
               'news': news,
               # 'advisers': advisers,
               'teammates': teammates,
               }
    if request.LANGUAGE_CODE == 'ru':
        return render(request, 'index.html', context)
    else:
        return render(request, 'index_en.html', context)


@gzip_page
def blockchain(request):
    services = Services.objects.all()
    emer_blocks = AboutEmer.objects.all()
    context = {
        'services': services,
        'emer_blocks': emer_blocks,
    }
    if request.LANGUAGE_CODE == 'ru':
        return render(request, 'emercoin-blockchain.html', context)
    else:
        return render(request, 'emercoin-blockchain_en.html', context)


@gzip_page
def tech_solutions(request):
    services = Services.objects.all()
    context = {
        'services': services,
    }
    if request.LANGUAGE_CODE == 'ru':
        return render(request, 'tech-solutions.html', context)
    else:
        return render(request, 'tech-solutions_en.html', context)


@gzip_page
def for_business(request):
    companies = Company.objects.all()
    context = {
        'companies': companies
    }
    if request.LANGUAGE_CODE == 'ru':
        return render(request, 'for-business.html', context)
    else:
        return render(request, 'for-business_en.html', context)


def for_coinholders(request):
    context = {}
    if request.LANGUAGE_CODE == 'ru':
        return render(request, 'for-coinholders.html', context)
    else:
        return render(request, 'for-coinholders_en.html', context)


@gzip_page
def for_developers(request):
    companies = Company.objects.all()
    services = Services.objects.all()
    context = {
        'companies': companies,
        'services': services,
    }
    if request.LANGUAGE_CODE == 'ru':
        return render(request, 'for-developers.html', context)
    else:
        return render(request, 'for-developers_en.html', context)


@gzip_page
def socials(request):
    news = News.objects.all()[:3]
    context = {
        'news': news,
    }
    if request.LANGUAGE_CODE == 'ru':
        return render(request, 'social-communities.html', context)
    else:
        return render(request, 'social-communities_en.html', context)


@gzip_page
def partners(request):
    companies_partners = Company.objects.filter(is_partner=True)
    companies_implements = Company.objects.filter(is_used=True)
    context = {
        'partners': companies_partners,
        'implements': companies_implements,
    }
    if request.LANGUAGE_CODE == 'ru':
        return render(request, 'partners-and-projects.html', context)
    else:
        return render(request, 'partners-and-projects_en.html', context)


@gzip_page
def company(request, slug):
    comp = get_object_or_404(Company, slug=slug)
    context = {'company': comp}
    if request.LANGUAGE_CODE == 'ru':
        return render(request, 'company.html', context)
    else:
        return render(request, 'company_en.html', context)


@gzip_page
def service(request, slug):
    one_service = get_object_or_404(Services, slug=slug)
    services = Services.objects.all()
    context = {
        'services': services,
        'one_service': one_service,
    }
    if request.LANGUAGE_CODE == 'ru':
        return render(request, 'service.html', context)
    else:
        return render(request, 'service_en.html', context)


@gzip_page
def team(request):
    persons = Person.objects.all()
    context = {
        'persons': persons
    }
    if request.LANGUAGE_CODE == 'ru':
        return render(request, 'team.html', context)
    else:
        return render(request, 'team_en.html', context)


@gzip_page
def news(request):
    if request.LANGUAGE_CODE == 'ru':
        news_list = News.objects.filter(title__isnull=False)
        page, paginator = get_paginated_view(request, news_list)
        context = {
            "page": page,
            "paginator": paginator,
        }
        return render(request, 'news.html', context)
    else:
        news_list = News.objects.filter(title_en__isnull=False)
        page, paginator = get_paginated_view(request, news_list)
        context = {
            "page": page,
            "paginator": paginator,
        }
        return render(request, 'news_en.html', context)


@gzip_page
def road_map(request):
    cnt = RoadMap.objects.count()
    roadmap = RoadMap.objects.all()[:cnt - 1]
    this_year = RoadMap.objects.last()
    context = {
        'roadmap': roadmap,
        'this_year': this_year,
    }
    if request.LANGUAGE_CODE == 'ru':
        return render(request, 'roadmap.html', context)
    else:
        return render(request, 'roadmap_en.html', context)


@gzip_page
def post(request, slug):
    """Страница отдельной новости"""
    one_post = get_object_or_404(News, slug=slug)
    context = {'post': one_post}
    if request.LANGUAGE_CODE == 'ru':

        return render(request, 'post.html', context)
    else:

        return render(request, 'post_en.html', context)


@requires_csrf_token
def page_not_found(request, exception):
    return render(request, 'misc/404.html', {"path": request.path}, status=404)


@requires_csrf_token
def server_error(request):
    return render(request, "misc/500.html", status=500)


@requires_csrf_token
def contacts(request):
    blank_page = get_blank_page(request)
    form = ContactForm()
    context = {
        'form': form,
        'sent': False,
        'blank': blank_page,
        'is_ru': is_lang_rus(request),
        'captcha_id': GOOGLE_RECAPTCHA_ID
    }
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if request.recaptcha_is_valid:
            if form.is_valid():
                send_support(form)
                context['sent'] = True
                return render(request, 'contacts.html', context)
        context['form'] = form

    if request.GET.get('sent'):
        context['sent'] = True
    return render(request, 'contacts.html', context)


@gzip_page
def rate(request):
    blank_page = get_blank_page(request)
    context = {
        'blank': blank_page,
        'is_ru': is_lang_rus(request),
    }
    return render(request, 'rate.html', context)


def terms(request):
    term = Terms.objects.last()
    blank_page = get_blank_page(request)
    context = {
        'blank': blank_page,
        'is_ru': is_lang_rus(request),
        'terms': term,
    }
    return render(request, 'misc/terms.html', context)


def privacy(request):
    priv = Privacy.objects.last()
    blank_page = get_blank_page(request)
    context = {
        'blank': blank_page,
        'is_ru': is_lang_rus(request),
        'privacy': priv,
    }
    return render(request, 'misc/privacy.html', context)
