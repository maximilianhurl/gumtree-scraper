from scrapy.exceptions import DropItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project.models import Advert
import scrapy


class AdvertItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    location = scrapy.Field()
    posted_date = scrapy.Field()
    url = scrapy.Field()


class AdvertPipeline(object):

    def open_spider(self, spider):
        engine = create_engine('sqlite:///listings.db')
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.commit()

    def process_item(self, item, spider):
        if self.session.query(Advert).filter(Advert.id == item['id']).count():
            # drop any adverts that have already been created
            raise DropItem("advert already in db %s" % item)

        advert = Advert(
            id=item['id'],
            title=item['title'],
            description=item['description'],
            price=item['price'],
            location=item['location'],
            posted_date=item['posted_date'],
            url=item['url'],
            processed=False,
        )

        self.session.add(advert)
