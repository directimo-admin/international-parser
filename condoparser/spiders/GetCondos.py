import datetime
import logging

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request

from condoparser.jpa.Source import Source
from condoparser.model.CondoDTO import CondoDTO
from services.MongoUtils import get_database

LOGGER = logging.getLogger(__name__)
dbname = get_database()
collection_name = dbname["condo-data"]

# Spider that gets condos


class GetCondos(scrapy.Spider):
    name = 'getCondosSpider'

    def __init__(self, *args, **kwargs):
        self.jobId = kwargs.get('_job')
        self.condoList = []
        self.config = Source.query.filter_by(
            name=kwargs.get('source')).first().config

    def start_requests(self):
        yield scrapy.Request(url=self.config["SOURCE"]["CONDOS_URL"], callback=self.parse)

    def parse(self, response):
        base_url = self.config["SOURCE"]["BASE_URL"]
        soup = BeautifulSoup(response.text, 'lxml')

        yield Request(response.url, callback=self.parsePage)

        # Verifies if need to use pagination logic or not
        if self.config["SOURCE"]["PAGINATION"] is True:
            # Get all pages of condos
            for item in soup.select(
                    self.config["SOURCE"]["DATA"]["CONDOS_PAGINATION_SELECTOR_URL"]):
                if item.attrs.get(
                        "class") is None or 'active' not in item.attrs.get("class"):
                    yield Request(base_url + item['href'], callback=self.parsePage)

    def parsePage(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        for item in soup.select(
                self.config["SOURCE"]["DATA"]["CONDOS_SELECTOR"]):
            url = item.a['href'].replace(
                self.config["SOURCE"]["CONDO_OFFERS_URL_REPLACE"],
                '') + self.config["SOURCE"]["CONDO_OFFERS_URL_SUFIX"]
            self.condoList.append(CondoDTO.slotted_to_dict(
                CondoDTO(url.split('/')[-2], url)))
        yield

    def closed(self, reason):
        collection_name.insert_one({
            "_id": self.jobId,
            "data": self.condoList,
            "processStatus": "CONDOS_FETCHED",
            "time": datetime.datetime.now(),
            "source": "imobiliare"
        })
