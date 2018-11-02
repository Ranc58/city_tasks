#!/bin/sh

bash ./wait-for-it.sh postgres:5432 -t 30
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000
