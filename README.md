# Emercoin Site
Сайт Emercoin

#### Пару слов о решении

Этот сайт был перенесен с laravel на django. Идея такая - никаких веб админок, всё правим и добавляем локально, пушим в dev в ветку гита, смотрим на dev.emercoin.com, если всё ок - делаем пул реквест в master и сайт разворачивается на основной домен.
Сайт запакован в контейнеры Docker: Django, базу данных [Postgresql](https://www.postgresql.org) и вебсервер [NGINX](https://nginx.org). Деплой автоматизирован через Github Workflow.

#### Настройка локальной машины нового разработчика с нуля.

Установить Docker и Docker-Compose

`sudo apt install docker && sudo apt install docker-compose`

Скачать гит:

`git pull https://github.com/mechnotech/emercoin && cd emercoin`

Создать и активировать окружение:

`python3 -m venv venv && source /venv/bin/activate`

`pip install -r requirements.txt`

В корне проекта создать файл .env по аналогии с .env.example

Создаем контейнер базы данных для локальной работы, заливаем миграции и последние фикстуры

`docker-compose -f local-postgres.yaml up -d`

`python manage.py migrate`

`sh load.sh`

Создаем админа для локальной версии сайта

`python manage.py createsuperuser`

Запускаем локальный сайт:

`python manage.py runserver 0.0.0.0:8000`

Теперь сайт доступен по адресу  http://0.0.0.0:8000/ ,админка  http://0.0.0.0:8000/admin

В админке можно добавлять новости, документацию, сми, партнеров, персоны и т.д. Исправлять шаблоны сайта и код луше всего в [Pycharm](https://www.jetbrains.com/ru-ru/pycharm/)

#### После внесения изменений, порядок действий:

Если менялись записи в базе - выгрузить их в fixtures.json

`python manage.py dumpdata --exclude auth.permission --exclude contenttypes --exclude auth.user --exclude sessions.session --exclude admin.logentry > fixtures.json`

либо исполнив скрипт *dump.sh*

Проверить код проекта $ flake8

Закомитить измненения и отправить в dev ветку github'a.

## Деплой

Установка автоматическая при push в репозиторий Github с помощью Github Workflow (см файлы emersite-workflow.yaml и devsite-workflow.yaml в папке .github/workflow!)
В нем описаны переменные типа ${{ secrets.SOME_VAR }} - эти переменные надо заданы в разделе settings репозитория Github
Если нужно поменять dev или product - сервер, следует изменить переменые:

>- DEV_TEST_HOST
>- TEST_HOST_ADMIN
>- SSH_KEY
>- ...

Соответственно настройкам серверов, куда будет развернут проект.

Следует отметить, что данный деплой испольует DockerHub для хранения образа сайта и в случае смены аккаунта Docker, нужно будет именить секреты и в этих переменных

### Dev и Product сервера

Перед тем как приступить к разворачиванию проекта, необходимо создать 2 VPS(виртуальный сервер) c доступом по ключу SSH (На сервера - публчный, в github secrets - приватный!)
После создания виртуалной машины, необходимо подготовить её:

- установить docker, docker-compose `sudo apt install -y docker.io docker-compose`

### Решения

Большинство нового контента создается через админку Django. 
Но существует сложность при создании новых документов в разделе "Документация".

Например, мы хотим добавить новый документ "Известные ошибки"(Known bugs):

В админке добавляем новую записть в "Документация", Заполняем поля: 

- Slug - URL: - "**known-bugs**", и русский и английский вариант текста документа.

 В файле emercoin/settings.py в список MENU добавляем элемент меню в конец списка (если нужно добавить узел меню, то вместо ключа url ставим ключ toggle, со знаением - список и в этот список добавляем элемент меню)

```
    {
        'name': 'Известные ошибки',
        'name_en': 'Known Bugs',
        'active': False,
        'url': 'known-bugs'
    },
```

Переходим в emerdocs/urls.py и в добавляем к списку urlpatterns

` path('known-bugs/', views.known_bugs, name='known-bugs')`


Теперь переходим в emerdocs/views.py и создаем функцию:

```
def known_bugs(request):
    return render_docs(request)

```

Выгрузить базу `sh dump.sh`

Проверить код с помощью flake8 код на стиль и сделать коммит.