web: gunicorn config.wsgi
web: python src/manage.py test --liveserver=0.0.0.0:$PORT
release: python manage.py migrate accounts && python manage.py migrate