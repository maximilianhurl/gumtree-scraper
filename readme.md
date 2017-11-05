# Gumtree scraper

Scrape gumtree looking for wardrobes in Brighton and Hove. Send daily reports for any in my price range and store in a database. 

## Setup 

    python3 -m venv env
    env/bin/pip install -r requirements.txt

## Generating migrations

     PYTHONPATH='.' alembic revision --autogenerate -m "Initial migration"
     alembic upgrade head

## Running spider

    scrapy runspider project/spider.py

## To Do

- add spider for pulling that loads search page
    + Should follow all links to detail pages when age is less than 24 hours and title contains 'wardrobe'

- Return items from spider
- Create pipeline that saves new items into the database

- Add airflow that
    + runs scrapy
        * set `dag.catchup = False`
    + generates report afterwards
    + Error handling task if either fail that returns error logs