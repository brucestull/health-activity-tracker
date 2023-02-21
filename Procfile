web: gunicorn config.wsgi
web: python manage.py test
release: python manage.py migrate accounts && python manage.py migrate