web: gunicorn gscrap.wsgi --timeout 400 --log-file -
worker: celery -A gscrap worker -l DEBUG --loglevel=info 
