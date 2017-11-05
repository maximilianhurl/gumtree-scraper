from datetime import datetime, timedelta
import scrapy
import logging
import re


def dehumanise_date(date: str):
    # given a string like '10 days ago' or '1 hour ago' returns a datetime
    matches = re.search("^(?P<value>[\d]+)\s(?P<unit>[\w]+)\sago", date.strip())
    if matches:
        value = matches.group('value')
        unit = matches.group('unit').rstrip('s')
        return datetime.now() - timedelta(**{f'{unit}s': int(value)})
    return None


class GumtreeSearchSpider(scrapy.Spider):
    name = "gumtree_search_spider"

    LISTING_SEARCH_SELECTOR = '.listing-maxi'

    start_urls = [
        'https://www.gumtree.com/search?search_category=beds-bedroom-furniture&search_location=brighton&search_scope=true',
        #'https://www.gumtree.com/search?search_category=beds-bedroom-furniture&search_location=hove&search_scope=true',
    ]

    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 0.2,
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

    def parse(self, response):

        listings = response.css(self.LISTING_SEARCH_SELECTOR)

        if listings:
            for listing in listings:
                link = listing.css('.listing-link::attr(href)')[0].extract()
                date = listing.css('.listing-posted-date span::text')[-1].extract()

                if '/' in link:  # skip the fake listings
                    print(link)
                    print('   HUMANISE')
                    print(dehumanise_date(date))
                    print('---------')
                    return

        else:
            logging.error("No listings found (Markup changed?)")
