FROM python:3
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE hra.settings.production
ENV SECRET_KEY this-is-not-a-secret
ENV STATIC_DIR /app/static
RUN apt update && apt install -y python3-psycopg2
RUN mkdir /app
WORKDIR /app
RUN mkdir /var/log/django
ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
ADD manage.py /app/manage.py
ADD public /app/public
ADD hra /app/hra
RUN python manage.py collectstatic
ADD version.txt /app/version.txt


EXPOSE 80

ENV Name HRA

CMD uwsgi --chdir /app --master --processes 4 --threads 2 --http-socket :80 --wsgi-file hra/wsgi.py
