from condoparser.model.CondoDTO import CondoDTO
import datetime
import logging

import pymongo
from sqlalchemy import desc

from condoparser.jpa import db
from condoparser.jpa.Condo import Condo
from condoparser.jpa.Offer import Offer
from condoparser.jpa.Source import Source
from condoparser.jpa.Status import Status
from condoparser.model.OfferDTO import OfferDTO
from services.MongoUtils import get_database

LOGGER = logging.getLogger(__name__)
dbname = get_database()
collection_name = dbname["condo-data"]


def insertAndGetId(item):
    db.session.add(item)
    db.session.flush()
    db.session.refresh(item)


def getStatusByName(name):
    return Status.query.filter_by(name=name).first()


def updateRecordStatus(oldStatus, newStatus):
    db.session.query(Offer).filter(Offer.record_status_id == getStatusByName(
        oldStatus).id).update({"record_status_id": getStatusByName(newStatus).id})
    db.session.commit()


def saveOffers(element, source, condo_id):
    parentId = None
    # NEW - to be created offers
    offer = Offer.query.filter_by(
        url=element['url'],
        record_status_id=getStatusByName('EXISTING').id).order_by(
        desc(
            Offer.created_at)).first()

    if offer is not None:
        if offer.parent_id is not None:
            parentOfParent = Offer.query.get(offer.parent_id)
            # PROCESSED status for records that was processed
            parentOfParent.parent_id = None
            parentOfParent.record_status_id = getStatusByName('PROCESSED').id
            parentOfParent.updated_at = datetime.datetime.now()
            insertAndGetId(parentOfParent)
        parentId = offer.id

    # NEW status for just added records
    return OfferDTO.toJpa(
        element,
        getStatusByName('NEW'),
        source,
        parentId,
        condo_id)


def saveCondosAndOffers(element, data):
    mongoId = data['_id']
    source = Source.query.filter_by(name='Imobiliare').first()
    condo = Condo.query.filter_by(url=element['url']).first()
    new_status = getStatusByName('NEW')
    if condo is None:
        condo = CondoDTO.toJpa(element, new_status, source, mongoId)
        insertAndGetId(condo)
        collection_name.update_one({"_id": mongoId},
                                   {'$set': {"data.$[idx].sql_id": condo.id}},
                                   upsert=False,
                                   array_filters=[{"idx.url": element['url']}])

    mappedOffers = list(map(lambda x: saveOffers(
        x, source, condo.id), element['offers']))
    db.session.bulk_save_objects(mappedOffers, return_defaults=True)
    db.session.commit()
    for offer in mappedOffers:
        collection_name.update_one({"_id": mongoId},
                                   {'$set': {"data.$[condoIdx].offers.$[offerIdx].sql_id": offer.id}},
                                   upsert=False,
                                   array_filters=[{"condoIdx.url": element['url']},
                                                  {"offerIdx.url": offer.url}])


if __name__ == '__main__':
    dataToBeProcessed = collection_name.find_one(
        {'processStatus': 'FINISHED'}, sort=[('time', pymongo.DESCENDING)])

    updateRecordStatus('EXISTING', 'PROCESSED')
    updateRecordStatus('NEW', 'EXISTING')

    list(map(lambda x: saveCondosAndOffers(
        x, dataToBeProcessed), dataToBeProcessed['data']))
