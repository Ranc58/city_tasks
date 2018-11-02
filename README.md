# City tasks
[![Coverage Status](https://coveralls.io/repos/github/Ranc58/city_tasks/badge.svg?branch=feature%2Ftasks_api)](https://coveralls.io/github/Ranc58/city_tasks?branch=feature%2Ftasks_api)
[![Build Status](https://travis-ci.org/Ranc58/city_tasks.svg?branch=master)](https://travis-ci.org/Ranc58/city_tasks)

Training project 

# How to install

1) With docker:
    - `cp env/.env_orig env/.env`
    - If it need - setup postgres in `env/.env` file. By default, this file is configured for use with Docker.
    - `docker-compose up --build`.
    - For run tests `docker-compose exec app python3 manage.py test`. \
    Postgres data will be saved in `postgres/pgdata`
    
2) Without docker:
    - Recomended use venv or virtualenv for better isolation.\
      Venv setup example: \
      `python3 -m venv myenv`\
      `source myenv/bin/activate`
    - `cp env/.env_orig src/.env;  cd src/`.
    - Setup postgres in `.env` file.
    - `pip3 install -r requirements.txt`
    - Run django `./run_server.sh`.
    - For run tests (from `src`) `python3 manage.py test`.
    

  