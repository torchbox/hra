FROM python:3
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE hra.settings.production
ENV SECRET_KEY this-is-not-a-secret
ENV LOG_DIR /var/log/django
ENV STATIC_DIR /app/static
RUN apt update && apt install -y python3-psycopg2
RUN mkdir /app
WORKDIR /app
RUN mkdir /var/log/django
ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
ADD manage.py /app/manage.py
ADD hra /app/hra
ADD start.sh /app/start.sh
RUN chmod +x /app/start.sh
ADD public /app/public


RUN python manage.py collectstatic

EXPOSE 80

ENV Name HRA

CMD /app/start.sh
