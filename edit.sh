#!/usr/bin/env bash
# Локальная админка Django для правки контента сайта.
# БД — временный SQLite, наполняется из fixtures.json (источник правды в git).
# После правок выполни ./publish.sh "сообщение".
#
#   ./edit.sh        → http://localhost:8000/admin/   (логин admin / пароль admin)
#
set -euo pipefail
cd "$(dirname "$0")"

IMAGE=emer-build:py310

# Собрать build-образ один раз, если его нет (нужен Python 3.10 + зависимости).
if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
  echo "Building $IMAGE (one-time)..."
  docker build -t "$IMAGE" -f - . <<'DOCKER'
FROM python:3.10-slim
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -q -r requirements.txt
DOCKER
fi

# Свежая БД из fixtures.json на каждый сеанс (детерминированно, без дрейфа).
rm -f local.sqlite3

echo "Admin: http://localhost:8000/admin/   (admin / admin)"
echo "Новость на английском: заполни Title (en), News text (en), Дата, News image."
echo "Ctrl-C — остановить. Затем: ./publish.sh \"add news X\""

docker run --rm -it -p 8000:8000 -v "$PWD":/code -w /code \
  -e DEBUG=True \
  -e DB_ENGINE=django.db.backends.sqlite3 -e DB_NAME=/code/local.sqlite3 \
  -e DJANGO_SUPERUSER_USERNAME=admin \
  -e DJANGO_SUPERUSER_PASSWORD=admin \
  -e DJANGO_SUPERUSER_EMAIL=admin@example.com \
  "$IMAGE" bash -c "
    python manage.py migrate --noinput &&
    python manage.py loaddata fixtures.json &&
    (python manage.py createsuperuser --noinput 2>/dev/null || true) &&
    python manage.py runserver 0.0.0.0:8000"
