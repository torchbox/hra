#!/bin/bash

exec uwsgi \
    --chdir /app \
    --master \
    --processes \
    4 \
    --threads \
    2 \
    --http-socket :80 \
    --wsgi-file hra/wsgi.py

