web: gunicorn gscrap.wsgi --timeout 400 --log-file -
worker : celery worker --app=gscrap.tasks
