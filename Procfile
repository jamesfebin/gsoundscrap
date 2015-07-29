web: gunicorn gscrap.wsgi --timeout 400 --log-file -
worker : python manage.py celery -A proj worker -l info
