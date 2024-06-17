from flask import current_app
from config import mongo
from services.log_service import LogService

class CustomerService:
    def __init__(self):
        self.mongo = mongo
        self.log_service = LogService()

    def webhook_callback(self, data):
        self.log_service.create_log(None, None, "Webhook callback recieved successfully", 200, data)
        return data, 200

    def event1(self, data):
        self.log_service.create_log(None, None, "Event 1 recieved successfully", 200, data)
        return data, 200

    def event2(self, data):
        self.log_service.create_log(None, None, "Event 2 recieved successfully", 200, data)
        return  data, 200

    def event3(self, data):
        self.log_service.create_log(None, None, "Event 3 recieved successfully", 200, data)
        return data, 200
