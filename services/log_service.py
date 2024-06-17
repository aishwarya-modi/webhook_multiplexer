from bson.objectid import ObjectId
from flask import current_app
from config import mongo
from constants import (
    RESPONSE_CODE_ERROR, SUCCESS_MESSAGE, DATABASE_ERROR_MESSAGE,
    RESPONSE_CODE_SUCCESS
)
from exceptions import DatabaseError
import datetime

class LogService:
    def __init__(self):
        self.mongo = mongo

    def get_logs_collection(self):
        return self.mongo.webhook_db.logs

    def create_log(self, webhook_id, endpoint_id, status, response_code, response_body, timestamp=None):
        try:
            if timestamp is None:
                timestamp = datetime.datetime.utcnow().isoformat() + 'Z'
            log = {
                "webhook_id": webhook_id,
                "endpoint_id": endpoint_id,
                "status": status,
                "response_code": response_code,
                "response_body": response_body,
                "timestamp": timestamp
            }
            self.get_logs_collection().insert_one(log)
            return log, RESPONSE_CODE_SUCCESS
        except Exception as e:
            current_app.logger.error(f"Error creating log: {e}")
            raise DatabaseError(DATABASE_ERROR_MESSAGE)


