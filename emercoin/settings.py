from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', default='5xj52xgg71lp2')

DEBUG = False if os.getenv('DEBUG') == 'False' else True

if DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = ['emercoin.com', 'dev.emercoin.com', 'www.emercoin.com']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'colorfield',
    'ckeditor',
    'ckeditor_uploader',
    'info',
    'emerdocs',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'emercoin.urls'

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'emercoin.wsgi.application'

if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": os.getenv('DB_ENGINE'),
            "NAME": os.getenv('DB_NAME'),
            "USER": os.getenv('POSTGRES_USER'),
            "PASSWORD": os.getenv('POSTGRES_PASSWORD'),
            "HOST": '172.16.238.10',
            "PORT": os.getenv('DB_PORT'),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": os.getenv('DB_ENGINE'),
            "NAME": os.getenv('DB_NAME'),
            "USER": os.getenv('POSTGRES_USER'),
            "PASSWORD": os.getenv('POSTGRES_PASSWORD'),
            "HOST": os.getenv('DB_HOST'),
            "PORT": os.getenv('DB_PORT'),
        }
    }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 300,
        'OPTIONS': {
            'MAX_ENTRIES': 2000
        }
    }
}
CACHE_MIDDLEWARE_SECONDS = 300
# Кешируем основные статраницы
P_CACHE = 60 if not DEBUG else 1

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]

# Email
if DEBUG:
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'emails')
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('YA_LOGIN')
EMAIL_HOST_PASSWORD = os.getenv('YA_PASS')
SUPPORT = os.getenv('YA_SUPPORT')
GOOGLE_RECAPTCHA_SECRET_KEY = os.getenv('RECAPCHA_KEY')
GOOGLE_RECAPTCHA_ID = os.getenv('RECAPCHA_ID')

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
    ('es', 'Spanish'),
    ('ko', 'Korean'),
    ('ja', 'Japan'),
    ('de', 'German'),
    ('ar', 'Arabic'),
    ('vi', 'Vietnamese'),
)

CKEDITOR_CONFIGS = {
    'default':
        {
            "skin": "moono-lisa",
            "toolbar_Basic": [["Source", "-", "Bold", "Italic"]],
            "toolbar_Full": [
                [
                    "Styles",
                    "Format",
                    "Bold",
                    "Italic",
                    "Underline",
                    "Strike",
                    "SpellChecker",
                    'NumberedList',
                    'BulletedList',
                ],
                ["Link", "Unlink", "Anchor"],
                ["Image", "Iframe", "Table", "HorizontalRule"],
                ["TextColor", "BGColor"],
                ["SpecialChar"],
                ["Source"],
            ],
            "toolbar": "Full",
            "height": 291,
            "width": 835,
            "filebrowserWindowWidth": 940,
            "filebrowserWindowHeight": 725,
        }}

# Меню раздела docs emercoin
MENU = [
    {
        'name': 'Об Эмеркоине',
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
                        'name': 'Docker контейнер',
                        'name_en': 'Docker',
                        'url': 'docker',
                        'active': False,
                    },
                    {
                        'name': 'Комндная строка CLI',
                        'name_en': 'CLI daemon',
                        'url': 'cli-daemon',
                        'active': False,
                    },
                    # {
                    #     'name': 'Веб интерфейс',
                    #     'name_en': 'EmerWEB wallet',
                    #     'url': 'emerweb-wallet',
                    #     'active': False,
                    # },

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
            {
                'name': 'EmerCert',
                'name_en': 'EmerCert',
                'active': False,
                'toggle': [
                    {
                        'name': 'Trusted Diploma',
                        'name_en': 'Trusted Diploma',
                        'active': False,
                        'url': 'trusted-diploma'
                    }
                ]

            },
            {
                'name': 'File Validator',
                'name_en': 'File Validator',
                'url': 'fv',
                'active': False,
            },
            {
                'name': 'Randpay',
                'name_en': 'Randpay',
                'url': 'randpay',
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

# static
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'

APPEND_SLASH = True
