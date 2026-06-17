#!/usr/bin/env bash
# Публикация изменений контента:
#   1) dumpdata из локального SQLite -> fixtures.json
#   2) заливка новых картинок media/ -> Cloudflare R2 (ключи из .r2.env)
#   3) commit + push -> GitHub Actions пересоберёт статику и выкатит на dev
#
#   ./publish.sh "add news X"
#
set -euo pipefail
cd "$(dirname "$0")"

MSG="${1:-content update}"
IMAGE=emer-build:py310

if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
  echo "Образ $IMAGE не найден — запусти сначала ./edit.sh (он его соберёт)."; exit 1
fi
if [ ! -f local.sqlite3 ]; then
  echo "Нет local.sqlite3 — сначала поредактируй через ./edit.sh."; exit 1
fi

# 1. Дамп контента -> fixtures.json
docker run --rm -v "$PWD":/code -w /code \
  -e DEBUG=True -e DB_ENGINE=django.db.backends.sqlite3 -e DB_NAME=/code/local.sqlite3 \
  "$IMAGE" python manage.py dumpdata \
    --exclude auth.permission --exclude contenttypes --exclude auth.user \
    --exclude sessions.session --exclude admin.logentry --indent 2 -o fixtures.json
echo "✓ fixtures.json обновлён"

# 2. Заливка media -> R2 (rclone copy шлёт только новые/изменённые файлы)
if [ -f .r2.env ]; then
  set -a; . ./.r2.env; set +a
  docker run --rm -v "$PWD/media":/m \
    -e RCLONE_CONFIG_R2_TYPE=s3 -e RCLONE_CONFIG_R2_PROVIDER=Cloudflare \
    -e RCLONE_CONFIG_R2_ACCESS_KEY_ID="$R2_ACCESS_KEY_ID" \
    -e RCLONE_CONFIG_R2_SECRET_ACCESS_KEY="$R2_SECRET_ACCESS_KEY" \
    -e RCLONE_CONFIG_R2_ENDPOINT="$R2_ENDPOINT" \
    -e RCLONE_CONFIG_R2_REGION=auto \
    rclone/rclone copy /m r2:"$R2_BUCKET" --ignore-existing \
      --header-upload "Cache-Control: public, max-age=604800" --s3-no-check-bucket
  echo "✓ media синхронизировано с R2 (r2:$R2_BUCKET)"
else
  echo "⚠ .r2.env не найден — заливка в R2 пропущена (см. .r2.env.example)"
fi

# 3. Commit + push
git add -A
if git diff --cached --quiet; then
  echo "Изменений для коммита нет."
else
  git commit -m "$MSG"
  git push
  echo "✓ Запушено — GitHub Actions пересоберёт и выкатит."
fi
