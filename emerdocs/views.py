from django.shortcuts import render, redirect


def about_emercoin(request):
    context = {}
    if request.LANGUAGE_CODE == 'ru':
        return render(request, 'about-emercoin.html', context)
    else:
        return render(request, 'about-emercoin_en.html', context)


def about_redirect(request):
    return redirect('about-emercoin/')


def intro_currency(request):
    context = {
        'intro': True,
        'emc_currency': True,
    }
    if request.LANGUAGE_CODE == 'ru':
        return render(request, 'introduction/the-emc-currency_en.html',
                      context)
    else:
        return render(request, 'introduction/the-emc-currency_en.html',
                      context)


def specifications(request):
    context = {
        'intro': True,
        'specs': True,
    }
    if request.LANGUAGE_CODE == 'ru':
        return render(request, 'introduction/specifications.html',
                      context)
    else:
        return render(request, 'introduction/specifications_en.html',
                      context)