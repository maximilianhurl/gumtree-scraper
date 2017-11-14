# Gumtree scraper

Scrape gumtree looking for wardrobes in Brighton and Hove. Send daily reports for any in my price range and store in a database. 

## Setup 

    python3 -m venv env
    env/bin/pip install -r requirements.txt

### Create databases (Postgres)

    createdb gumtree_scraper
    createdb airflow

### Environment vars

    export DB_URL=postgres://localhost/gumtree_scraper
    export AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgres://localhost/airflow
    export PYTHONPATH='.'
    export AIRFLOW_HOME='.'
    export MAILGUN_KEY=SUPER-SEKRIT-KEY-HERE

### Generating/running migrations

     alembic revision --autogenerate -m "Initial migration"
     alembic upgrade head

### Running spider

    scrapy runspider project/spider.py

### Airflow

    airflow initdb
    airflow webserver -p 8080
    airflow scheduler

## Docker

### Build the docker image

    docker build -t gumtree-scraper .

### Create network bridge for database

    docker network create --driver bridge isolated-gumtree-scraper

### Create and run two postgres databases using the network bridge

    docker run -i -t --init --rm --name gumtree-postgres --network=isolated-gumtree-scraper -e POSTGRES_PASSWORD=password -e POSTGRES_DB=gumtree_scraper -d postgres

    docker run -i -t --init --rm --name gumtree-postgres-airflow --network=isolated-gumtree-scraper -e POSTGRES_PASSWORD=password -e POSTGRES_DB=airflow -d postgres

### Migrate the databases

    docker run -i -t --init --rm --network isolated-gumtree-scraper --name gumtree-scraper -p 8001:8080 -e DB_URL=postgres://postgres:password@gumtree-postgres/gumtree_scraper -e AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgres://postgres:password@gumtree-postgres-airflow/airflow -e MAILGUN_KEY=SUPER-SEKRIT-KEY-HERE gumtree-scraper "env/bin/alembic upgrade head && env/bin/airflow initdb"

### Run the web server and worker

    docker run -i -t --init --rm --network isolated-gumtree-scraper --name gumtree-scraper -p 8001:8080 -e DB_URL=postgres://postgres:password@gumtree-postgres/gumtree_scraper -e AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgres://postgres:password@gumtree-postgres-airflow/airflow -e MAILGUN_KEY=SUPER-SEKRIT-KEY-HERE gumtree-scraper "env/bin/airflow webserver -p 8080 && env/bin/airflow scheduler"

## To Do

- deploy to dokku
