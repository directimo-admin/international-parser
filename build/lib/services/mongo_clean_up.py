from datetime import datetime, timedelta

from services.MongoUtils import get_database

dbname = get_database()
condo_collection = dbname["condo-data"]
html_collection = dbname["html-data"]


if __name__ == '__main__':
    condo_collection.delete_many({'time':{'$lt': datetime.now() - timedelta(days=30)}})
    html_collection.delete_many({'time':{'$lt': datetime.now() - timedelta(days=30)}})
