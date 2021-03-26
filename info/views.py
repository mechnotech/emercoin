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
    return render(
        request,
        'index.html',
        {'promos': promos,
         'emer_blocks': emer_blocks,
         'services': services,
         'medium': medium,
         'roadmap': roadmap,
         'news': news,
         'advisers': advisers,
         'teammates': teammates,
         }
    )
