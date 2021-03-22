from django.shortcuts import render
from .models import Promo, AboutEmer, Services


def index(request):
    promos = Promo.objects.all()[:10]
    emer_blocks = AboutEmer.objects.all()
    services = Services.objects.all()
    return render(
        request,
        'index.html',
        {'promos': promos,
         'emer_blocks': emer_blocks,
         'services': services,
         }
    )
