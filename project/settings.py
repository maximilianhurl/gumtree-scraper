from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import environ

BASE_URL = 'https://www.gumtree.com'

SEARCH_KEYWORDS = [
    'wardrobe',
    'warbrobe',
    'wardrob'
]

# TODO: Pass these as params to DAG
SEARCH_URLS = [
    f'{BASE_URL}/search?search_category=beds-bedroom-furniture&search_location=brighton&search_scope=true',
    f'{BASE_URL}/search?search_category=beds-bedroom-furniture&search_location=hove&search_scope=true',
]

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'

DB_URL = environ['DB_URL']

REPORT_EMAIL = 'max@maxhurl.co.uk'
MAILGUN_KEY = environ['MAILGUN_KEY']
MAILGUN_URL = 'https://api.mailgun.net/v2/sandboxb7645bd943614e39bb23ef85318eb9e1.mailgun.org/messages'


def create_sqlalchemy_engine():
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    return engine, Session


def commit_session(session):
    try:
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
