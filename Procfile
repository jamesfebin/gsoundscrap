web: gunicorn gscrap.wsgi --timeout 400 --log-file -
worker: celery -A gscrapweb.tasks worker --loglevel=info --concurrency=1

