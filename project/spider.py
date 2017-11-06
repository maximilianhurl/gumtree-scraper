from datetime import datetime, timedelta
from project.pipelines import AdvertItem
from typing import Optional
import scrapy
import logging
import re


SEARCH_KEYWORDS = [
    'wardrobe',
    'warbrobe',
    'wardrob'
]


def dehumanise_date(date: str) -> Optional[datetime]:
    # given a string like '10 days ago' or '1 hour ago' returns a datetime
    matches = re.search("^(?P<value>[\d]+)\s(?P<unit>[\w]+)\sago", date.strip())
    if matches:
        value = matches.group('value')
        unit = matches.group('unit').rstrip('s').replace('min', 'minute')
        return datetime.now() - timedelta(**{f'{unit}s': int(value)})

    elif date.lower().strip() == 'just now':
        return datetime.now()

    return None


def get_ad_id_from_url(url: str) -> Optional[str]:
    return url.rsplit('/', 1)[-1]


def is_valid_posted_date(posted_date: datetime) -> bool:
    if posted_date > datetime.now() - timedelta(hours=24, minutes=1):
        return True
    return False


def is_relevant_title(title: str) -> bool:
    if any(keyword in title.lower() for keyword in SEARCH_KEYWORDS):
        return True
    return False


def remove_whitespace(string: str) -> str:
    return string.replace('\r', '').replace('\n', '').strip()


class GumtreeSearchSpider(scrapy.Spider):
    name = "gumtree_search_spider"

    BASE_URL = 'https://www.gumtree.com'
    start_urls = [
        f'{BASE_URL}/search?search_category=beds-bedroom-furniture&search_location=brighton&search_scope=true',
        f'{BASE_URL}/search?search_category=beds-bedroom-furniture&search_location=hove&search_scope=true',
    ]

    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 0.2,
        'ITEM_PIPELINES': {
            'project.pipelines.AdvertPipeline': 800,
        },
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

    def parse(self, response):
        adverts = response.css('.listing-maxi')

        if adverts:
            for advert in adverts:
                link = advert.css('.listing-link::attr(href)')[0].extract()
                if '/' in link:  # skip the fake listings
                    human_posted_date = advert.css('.listing-posted-date span::text')[-1].extract()
                    posted_date = dehumanise_date(human_posted_date)
                    title = remove_whitespace(advert.css('.listing-title::text')[0].extract())

                    if is_relevant_title(title) and is_valid_posted_date(posted_date):
                        yield scrapy.Request(
                            f'{self.BASE_URL}{link}',
                            callback=self.parse_ad_detail,
                            meta={
                                'title': title,
                                'posted_date': posted_date,
                            }
                        )
        else:
            logging.error("No adverts found (Markup changed?)")

    def parse_ad_detail(self, response):
        location = response.css('.ad-location span::text')[0].extract().split(',')[0]
        price = remove_whitespace(response.css('.ad-price::text')[0].extract().replace('£', ''))
        description = remove_whitespace(' '.join(response.css('.ad-description::text').extract()))

        yield AdvertItem(
            id=response.url.split('/')[-1].strip(),
            title=response.request.meta['title'],
            description=description,
            price=price,
            location=location,
            posted_date=response.request.meta['posted_date'],
            url=response.url
        )
