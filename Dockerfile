FROM python:3.6-slim
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE hra.settings.production
ENV SECRET_KEY this-is-not-a-secret
ENV STATIC_DIR /app/static
#RUN apt update && apt install -y python3-psycopg2
RUN apt update && apt install -y build-essential zlib1g-dev libjpeg-dev
COPY k8s-safe-cronjob /sbin
RUN mkdir /app
WORKDIR /app
RUN mkdir /var/log/django
ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
ADD manage.py /app/manage.py
ADD version.txt /app/version.txt
ADD public /app/public
ADD hra /app/hra
RUN python /app/manage.py collectstatic --noinput


EXPOSE 80

ENV Name HRA

CMD uwsgi --disable-logging --chdir /app --master --processes 1 --threads 2 --http-socket :80 --wsgi-file hra/wsgi.py
