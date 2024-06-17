from config import mongo
from constants import WEBHOOK_COLLECTION, LOGS_COLLECTION

def get_webhook_collection():

    return mongo.db[WEBHOOK_COLLECTION]

def get_logs_collection():
    return mongo.db[LOGS_COLLECTION]
