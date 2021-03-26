from django.shortcuts import render
from .models import Promo, AboutEmer, Services, Media, RoadMap, News, Person


def index(request):
    promos = Promo.objects.all()[:10]
    emer_blocks = AboutEmer.objects.all()
    services = Services.objects.all()
    medium = Media.objects.all()
    roadmap = RoadMap.objects.all()
    news = News.objects.all()[:3]
    advisers = Person.objects.filter(is_adviser=True)
    teammates = Person.objects.filter(is_team=True)
    context = {'promos': promos,
         'emer_blocks': emer_blocks,
         'services': services,
         'medium': medium,
         'roadmap': roadmap,
         'news': news,
         'advisers': advisers,
         'teammates': teammates,
         }
    if request.LANGUAGE_CODE == 'ru':
        return render(request, 'index.html', context)
    else:
        return render(request, 'index_en.html', context)


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


def tech_solutions(request):
    services = Services.objects.all()
    context = {
        'services': services,
    }
    if request.LANGUAGE_CODE == 'ru':
        return render(request, 'tech-solutions.html', context)
    else:
        return render(request, 'tech-solutions_en.html', context)