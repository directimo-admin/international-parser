import datetime
import logging

import htmlmin
import jsonpickle
import scrapy
from bs4 import BeautifulSoup

from condoparser.jpa.Source import Source
from services.MongoUtils import get_database

LOGGER = logging.getLogger(__name__)
dbname = get_database()
collection_name = dbname["condo-data"]
collection_html = dbname["html-data"]
jsonpickle.set_encoder_options('json', ensure_ascii=False)


def findElementInDetails(root, fieldName):
    return root.find(
        lambda tag: tag.name == "li" and fieldName in tag.text)

# Spider that gets an offer and extract details


class GetOfferDetailsSpider(scrapy.Spider):
    name = 'getOfferDetailsSpider'

    def __init__(self, *args, **kwargs):
        self.jobId = kwargs.get('jobId')
        self.config = Source.query.filter_by(
            name=kwargs.get('source')).first().config

    def start_requests(self):
        global condoList

        currentObj = collection_name.find_one({"_id": self.jobId})
        condoList = currentObj['data']
        offerList = []

        for res in condoList:
            offerList.extend(res['offers'])

        urls = list(map(lambda element: element['url'], list(offerList)))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        global condoList
        soup = BeautifulSoup(response.text, 'lxml')
        # Check if the offer got expired
        expired = True if soup.select(
            self.config["SOURCE"]["DATA"]["EXPIRED_SELECTOR"]) else False

        for res in condoList:
            offerToUpdate = next(
                filter(
                    lambda element: element['url'] == response.request.url,
                    res['offers']),
                None)

            if offerToUpdate is not None and expired is False:

                # Save html documents for audit purposes
                htmlObj = collection_html.insert_one({'data': htmlmin.minify(
                    response.text, remove_empty_space=True), "time": datetime.datetime.now()})

                primaryDetails = soup.select(
                    self.config["SOURCE"]["DATA"]["PROPERTIES_ROOT_SELECTOR"])[0]
                offerToUpdate['html_id'] = htmlObj.inserted_id

                offerToUpdate['bathroom_no'] = int(
                    findElementInDetails(
                        primaryDetails,
                        self.config["SOURCE"]["DATA"]["BATHROOM_NO_TEXT"]).span.text) if findElementInDetails(
                    primaryDetails,
                    self.config["SOURCE"]["DATA"]["BATHROOM_NO_TEXT"]) is not None else None
                offerToUpdate['usable_area'] = float(
                    findElementInDetails(
                        primaryDetails,
                        self.config["SOURCE"]["DATA"]["USABLE_AREA_TEXT"]).span.text.split(' ')[0].replace(
                        ',',
                        '.')) if findElementInDetails(
                    primaryDetails,
                    self.config["SOURCE"]["DATA"]["USABLE_AREA_TEXT"]) is not None else None
                offerToUpdate['room_no'] = int(
                    findElementInDetails(
                        primaryDetails,
                        self.config["SOURCE"]["DATA"]["ROOM_NO_TEXT"]).span.text) if findElementInDetails(
                    primaryDetails,
                    self.config["SOURCE"]["DATA"]["ROOM_NO_TEXT"]) is not None else None
                total_surface = float(
                    findElementInDetails(
                        primaryDetails,
                        self.config["SOURCE"]["DATA"]["TOTAL_USABLE_AREA_TEXT"]).span.text.split(' ')[0]) if findElementInDetails(
                    primaryDetails,
                    self.config["SOURCE"]["DATA"]["TOTAL_USABLE_AREA_TEXT"]) is not None else None
                offerToUpdate['terase_usable_area'] = total_surface - offerToUpdate[
                    'usable_area'] if total_surface is not None and offerToUpdate['usable_area'] is not None else None
                offerToUpdate['construction_date'] = int(
                    findElementInDetails(
                        primaryDetails,
                        self.config["SOURCE"]["DATA"]["CONSTRUCTION_DATE_TEXT"]).span.text.split(' ')[0]) if findElementInDetails(
                    primaryDetails,
                    self.config["SOURCE"]["DATA"]["CONSTRUCTION_DATE_TEXT"]) is not None else None

            elif offerToUpdate is not None and expired is True:
                res['offers'].remove(offerToUpdate)

            if offerToUpdate is not None:
                collection_name.update_one({"_id": self.jobId},
                                           {"$set": {
                                               "data": condoList}})

        yield

    def closed(self, reason):
        collection_name.update_one({"_id": self.jobId}, {
            "$set": {"processStatus": "FINISHED", "time": datetime.datetime.now(), }})
