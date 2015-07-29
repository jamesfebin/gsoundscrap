web: gunicorn gscrap.wsgi --timeout 400 --log-file -
worker : celery -A proj worker -l info
