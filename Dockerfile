FROM python:3
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE hra.settings.production
ENV SECRET_KEY this-is-not-a-secret
RUN mkdir /app
ADD requirements.txt /app/requirements.txt
ADD manage.py /app/manage.py
ADD hra /app/hra
ADD public /app/public

WORKDIR /app

RUN pip install -r requirements.txt
RUN python manage.py collectstatic

EXPOSE 80

ENV Name HRA

CMD ["uwsgi", "--chdir", "/app", "--master", "--processes", "4", "--threads", "2", "--http-socket", ":80", "--wsgi-file", "hra/wsgi.py"]

