web: gunicorn gscrap.wsgi --timeout 400 --log-file -
worker: celery -A gscrap.tasks worker --loglevel=info --concurrency=1

