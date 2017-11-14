# Gumtree scraper

Scrape gumtree looking for wardrobes in Brighton and Hove. Send daily reports for any in my price range and store in a database. 

## Setup 

    python3 -m venv env
    env/bin/pip install -r requirements.txt

## Create databases (Postgresql)

    createdb gumtree_scraper
    createdb airflow

## Environment vars

    export DB_URL=postgres://localhost/gumtree_scraper
    export AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgres://localhost/airflow
    export PYTHONPATH='.'
    export AIRFLOW_HOME='.'
    export MAILGUN_KEY=SUPER-SEKRIT-KEY-HERE

## Generating/running migrations

     alembic revision --autogenerate -m "Initial migration"
     alembic upgrade head

## Running spider

    scrapy runspider project/spider.py

## Airflow

    airflow initdb
    airflow webserver -p 8080
    airflow scheduler

## To Do

- add docker support
- deploy to dokku