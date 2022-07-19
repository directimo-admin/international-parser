import datetime
import logging

import scrapy
from bs4 import BeautifulSoup
from scrapy.utils import spider

from condoparser.jpa.Source import Source
from condoparser.model.OfferDTO import OfferDTO
from services.MongoUtils import get_database

LOGGER = logging.getLogger(__name__)
dbname = get_database()
collection_name = dbname["condo-data"]

# Spider that gets all offers per condo

class GetOffersSpider(spider.Spider):
    name = 'getOffersSpider'
    condoList = None

    def __init__(self, *args, **kwargs):
        self.jobId = kwargs.get('jobId')
        self.config = Source.query.filter_by(
            name=kwargs.get('source')).first().config

    def start_requests(self):
        global condoList

        currentObj = collection_name.find_one({"_id": self.jobId})
        condoList = currentObj['data']
        urls = list(map(lambda element: element['url'], condoList))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        global condoList
        soup = BeautifulSoup(response.text, 'lxml')
        offerList = []
        for item in soup.select(
                self.config["SOURCE"]["DATA"]["OFFERS_SELECTOR"]):
            price = item.select(".pret")[0].getText().split(" ")[
                0].replace('.', '')
            url = item.a['href']
            if int(price) > 10000 and "vanzare-case-vile" not in url and collection_name.find_one(
                    {"_id": self.jobId, "data.offers.url": url}) is None:
                offerList.append(OfferDTO.slotted_to_dict(
                    OfferDTO(url.split('/')[-1], url, int(price))))

        condoToUpdate = list(
            filter(
                lambda element: element['url'] == response.request.url,
                condoList))[0]
        condoToUpdate['offers'] = offerList
        condoToUpdate['zone'] = soup.select(
            self.config["SOURCE"]["CONDO_ZONE"])[0].text
        collection_name.update_one({"_id": self.jobId}, {
                                   "$set": {"data": condoList}})
        yield

    def closed(self, reason):
        collection_name.update_one({"_id": self.jobId}, {
            "$set": {"processStatus": "OFFERS_FETCHED", "time": datetime.datetime.now()}})
