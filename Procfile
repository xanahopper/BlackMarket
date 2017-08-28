web: gunicorn -b 127.0.0.1:5000 -w 3 app:app -k eventlet
celery_worker: celery -A task worker --loglevel=info
# celery_beat: celery beat -A task