from datetime import datetime, timedelta
from project.pipelines import AdvertItem
from project.settings import BASE_URL, SEARCH_KEYWORDS, SEARCH_URLS, USER_AGENT
from typing import Optional
import scrapy
import logging
import re


def dehumanise_date(date: str) -> Optional[datetime]:
    # given a string like '10 days ago' or '10 mins ago' returns a datetime
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
    return any(keyword in title.lower() for keyword in SEARCH_KEYWORDS)


def remove_whitespace(string: str) -> str:
    return string.replace('\r', '').replace('\n', '').strip()


class GumtreeSearchSpider(scrapy.Spider):
    name = "gumtree_search_spider"

    start_urls = SEARCH_URLS

    MARKUP_ERROR = "No adverts found (Markup changed?)"

    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 0.2,
        'ITEM_PIPELINES': {
            'project.pipelines.AdvertPipeline': 800,
        },
        'USER_AGENT': USER_AGENT
    }

    def parse(self, response):
        adverts = response.css('.listing-maxi')

        if not adverts:
            logging.error(self.MARKUP_ERROR)
            raise Exception(self.MARKUP_ERROR)

        for advert in adverts:
            link = advert.css('.listing-link::attr(href)')[0].extract()
            if '/' in link:  # skip the fake listings
                human_posted_date = advert.css('.listing-posted-date span::text').extract()
                if human_posted_date:  # skip those without dates as they are ads

                    posted_date = dehumanise_date(human_posted_date[-1])
                    title = remove_whitespace(advert.css('.listing-title::text')[0].extract())

                    if is_relevant_title(title) and is_valid_posted_date(posted_date):
                        yield scrapy.Request(
                            f'{BASE_URL}{link}',
                            callback=self.parse_ad_detail,
                            meta={
                                'title': title,
                                'posted_date': posted_date,
                            }
                        )

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
