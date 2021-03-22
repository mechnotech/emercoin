from django.shortcuts import render
from .models import Promo


def index(request):
    promos = Promo.objects.all()[:10]
    return render(request, 'index.html', {'promos': promos})
