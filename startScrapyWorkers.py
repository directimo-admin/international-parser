from time import sleep
import sys
import requests


spiderFlow = ['getCondosSpider', 'getOffersSpider', 'getOfferDetailsSpider']
initialJobId = None

import os
from dotenv import load_dotenv

load_dotenv('.env.local')
def triggerListJob():
    return requests.get(
         os.getenv("SCRAPY_URL") + "/listjobs.json?project=condoparser").json()


def checkIfJobCompleted(jobId):
    while next(
            filter(
                lambda element: element['id'] == jobId,
                triggerListJob()['finished']),
            None) is None:
        sleep(1)


def runSpiderJob(spiderName, source):
    global initialJobId
    response = requests.post(
        os.getenv("SCRAPY_URL") + "/schedule.json",
        data={
            'project': 'condoparser',
            'spider': spiderName,
            'jobId': initialJobId,
            'source': source})
    jobId = response.json()['jobid']

    initialJobId = jobId if initialJobId is None else initialJobId
    checkIfJobCompleted(jobId)
    return jobId


if __name__ == '__main__':
    source = None
    if not sys.argv[1:]:
        sys.exit("Please select the source")
    else:
        source = sys.argv[1:][0]

    for spider in spiderFlow:
        jobId = runSpiderJob(spider, source)
