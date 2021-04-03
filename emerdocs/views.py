from copy import copy

from django.shortcuts import render, redirect

MENU = [
    {
        'name': 'О Эмеркоине',
        'name_en': 'About Emercoin',
        'url': 'about-emercoin',
        'active': False,
    },
    {
        'name': 'Введение',
        'name_en': 'Introduction',
        'active': False,
        'toggle': [
            {
                'name': 'Криптовалюта EMC',
                'name_en': 'The EMC Currency',
                'url': 'the-emc-currency',
                'active': False,
            },
            {
                'name': 'Спецификации',
                'name_en': 'Emercoin Specifications',
                'url': 'specifications',
                'active': False,
            },
            {
                'name': 'Принципы безопасности Эмеркоин',
                'name_en': 'Emercoin Security Principles',
                'url': 'security-principles',
                'active': False,
            },
        ]
    },
    {
        'name': 'Установка',
        'name_en': 'Install Software',
        'active': False,
        'toggle': [
            {
                'name': 'Десктопные кошельки',
                'name_en': 'Core Wallets',
                'active': False,
                'toggle': [
                    {
                        'name': 'Графический интерфейс',
                        'name_en': 'GUI Wallets',
                        'url': 'gui-wallet',
                        'active': False,
                    },
                    {
                        'name': 'Комндная строка CLI',
                        'name_en': 'CLI daemon',
                        'url': 'cli-daemon',
                        'active': False,
                    },
                    {
                        'name': 'Веб интерфейс',
                        'name_en': 'EmerWEB wallet',
                        'url': 'emerweb-wallet',
                        'active': False,
                    },
                    {
                        'name': 'Docker контейнер',
                        'name_en': 'Docker',
                        'url': 'docker',
                        'active': False,
                    },

                ]
            },
            {
                'name': 'Другие кошельки',
                'name_en': 'Other wallets',
                'url': 'other-wallets',
                'active': False,
            },
        ]
    },
    {
        'name': 'Запуск',
        'name_en': 'Running Emercoin',
        'active': False,
        'toggle': [
            {
                'name': 'Быстрый старт linux',
                'name_en': 'Linux Quickstart',
                'url': 'linux-quickstart',
                'active': False,
            },
            {
                'name': 'Командная строка',
                'name_en': 'Command Line',
                'url': 'command-line',
                'active': False,
            },
            {
                'name': 'Файл emercoin.conf',
                'name_en': 'emercoin.conf file',
                'url': 'emercoin-conf',
                'active': False,
            },
            {
                'name': 'Порты',
                'name_en': 'Ports',
                'url': 'ports',
                'active': False,
            },
            {
                'name': 'Тестнет',
                'name_en': 'Тestnet',
                'url': 'testnet',
                'active': False,
            },
        ]
    },
    {
        'name': 'Эмеркоин API',
        'name_en': 'Emercoin API',
        'active': False,
        'url': 'emercoin-api'
    },
    {
        'name': 'Блокчейн сервисы',
        'name_en': 'Blockchain Services',
        'active': False,
        'toggle': [
            {
                'name': 'Введение в блокчейн сервисы Эмеркоин',
                'name_en': 'Introduction to Emercoin Services',
                'url': 'introduction-to-emercoin-services',
                'active': False,
            },
            {
                'name': 'EmerNVS',
                'name_en': 'EmerNVS',
                'url': 'emernvs',
                'active': False,
            },
            {
                'name': 'EmerSSH',
                'name_en': 'EmerSSH',
                'url': 'emerssh',
                'active': False,
            },
            {
                'name': 'EmerSSL',
                'name_en': 'EmerSSL',
                'active': False,
                'toggle': [
                    {
                        'name': 'Введение в технологию',
                        'name_en': 'EmerSSL Introduction',
                        'url': 'emerssl-introduction',
                        'active': False,
                    },
                    {
                        'name': 'Руководство EmerSSL',
                        'name_en': 'EmerSSL Guide',
                        'url': 'emerssl-guide',
                        'active': False,
                    },
                    {
                        'name': 'Инфокарта EmerSSL',
                        'name_en': 'EmerSSL Infocard',
                        'url': 'emerssl-infocard',
                        'active': False,
                    },

                ]
            },
            {
                'name': 'EmerDNS',
                'name_en': 'EmerDNS',
                'active': False,
                'toggle': [
                    {
                        'name': 'Введение в технологию',
                        'name_en': 'EmerDNS Introduction',
                        'url': 'emerdns-introduction',
                        'active': False,
                    },

                ]
            },
            {
                'name': 'EmerDPO',
                'name_en': 'EmerDPO',
                'active': False,
                'toggle': [
                    {
                        'name': 'Введение в технологию',
                        'name_en': 'EmerDPO Introduction',
                        'url': 'emerdpo-introduction',
                        'active': False,
                    },
                    {
                        'name': 'Программа Antifake',
                        'name_en': 'The EmerDPO Antifake Programme',
                        'url': 'the-emerdpo-antifake-programme',
                        'active': False,
                    },
                    {
                        'name': 'Программа SN-Publisher',
                        'name_en': 'EmerDPO SN-Publisher',
                        'url': 'emerdpo-sn-publisher',
                        'active': False,
                    },

                ]
            },
            {
                'name': 'EmerMAGNET',
                'name_en': 'EmerMAGNET',
                'url': 'emermagnet',
                'active': False,
            },
            {
                'name': 'ENUMer',
                'name_en': 'ENUMer',
                'url': 'enumer',
                'active': False,
            },
        ]
    },
    {
        'name': 'Создание блоков',
        'name_en': 'Block Generation',
        'active': False,
        'toggle': [
            {
                'name': 'Добыча Proof-of-Stake',
                'name_en': 'Proof-of-Stake Minting',
                'url': 'proof-of-stake-minting',
                'active': False,
            },
            {
                'name': 'Добыча Proof-of-Work',
                'name_en': 'Proof-of-Work Mining',
                'url': 'proof-of-work-mining',
                'active': False,
            },
        ]
    },
    {
        'name': 'Эмеркоин медиа-кит',
        'name_en': 'Emercoin Press Kit',
        'active': False,
        'url': 'emercoin-press-kit'
    },
    {
        'name': 'Ссылки и источники',
        'name_en': 'Links & Resources',
        'active': False,
        'url': 'links-resources'
    },

]


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
    menu = copy(MENU)
    return recursive(menu, url)[0]


def about_emercoin(request):
    url = request.resolver_match.url_name
    menu = activate(url)
    context = {
        'menu': menu
    }
    if request.LANGUAGE_CODE == 'ru':
        return render(request, 'about-emercoin.html', context)
    else:
        return render(request, 'about-emercoin_en.html', context)


def about_redirect(request):
    return redirect('about-emercoin/')


def intro_currency(request):
    context = {
        'menu': MENU,
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
    url = request.resolver_match.url_name
    menu = activate(url)

    context = {
        'menu': menu,
        'intro': True,
        'specs': True,
    }
    if request.LANGUAGE_CODE == 'ru':
        return render(request, 'introduction/specifications.html',
                      context)
    else:
        return render(request, 'introduction/specifications_en.html',
                      context)


def gui_wallet(request):
    url = request.resolver_match.url_name
    menu = activate(url)
    context = {
        'menu': menu
    }
    if request.LANGUAGE_CODE == 'ru':
        return render(request, 'about-emercoin_en.html',
                      context)
    else:
        return render(request, 'about-emercoin_en.html',
                      context)
