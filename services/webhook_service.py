import asyncio
from aiohttp import ClientSession
from bson.objectid import ObjectId
from flask import current_app
from config import mongo
from constants import (
    RESPONSE_CODE_ERROR, SUCCESS_MESSAGE, ENDPOINT_DELETED_MESSAGE, WEBHOOK_NOT_FOUND_MESSAGE,
    DATABASE_ERROR_MESSAGE, FORWARDING_ERROR_MESSAGE, UPTIME, AVERAGE_LATENCY_MS,
    RESPONSE_CODE_SUCCESS
)
from exceptions import DatabaseError, NotFoundError
import datetime
from services.log_service import LogService
import requests

class WebhookService:
    def __init__(self):
        self.mongo = mongo
        self.log_service = LogService()

    def get_webhook_collection(self):
        return self.mongo.webhook_db.webhooks

    def create_webhook(self, data):
        try:
            webhook = {
                "customer_id": data["customer_id"],
                "webhook_url": data["webhook_url"],
                "endpoints": []
            }
            result = self.get_webhook_collection().insert_one(webhook)
            if result.acknowledged:
                self.log_service.create_log(str(result.inserted_id), None, SUCCESS_MESSAGE, RESPONSE_CODE_SUCCESS, "Webhook created successfully")
            else:
                raise DatabaseError("Data not inserted into MongoDB")
            return {"webhook_id": str(result.inserted_id), "webhook_url": data["webhook_url"]}, RESPONSE_CODE_SUCCESS
        except Exception as e:
            self.log_service.create_log(None, None, None, RESPONSE_CODE_ERROR, f"Error creating webhook: {e}")
            raise DatabaseError(DATABASE_ERROR_MESSAGE)

    def add_endpoints(self, webhook_id, data):
        try:
            endpoints = data.get("endpoints", [])
            for endpoint in endpoints:
                endpoint["endpoint_id"] = str(ObjectId())
            self.get_webhook_collection().update_one(
                {"_id": ObjectId(webhook_id)},
                {"$addToSet": {"endpoints": {"$each": endpoints}}}
            )
            self.log_service.create_log(webhook_id, None, SUCCESS_MESSAGE, RESPONSE_CODE_SUCCESS, "Endpoints added successfully")
            return {"webhook_id": webhook_id, "endpoints": endpoints}, RESPONSE_CODE_SUCCESS
        except Exception as e:
            self.log_service.create_log(webhook_id, None, None, RESPONSE_CODE_ERROR, f"Error adding endpoints: {e}")
            raise DatabaseError(DATABASE_ERROR_MESSAGE)

    def delete_endpoint(self, webhook_id, endpoint_id):
        try:
            self.get_webhook_collection().update_one(
                {"_id": ObjectId(webhook_id)},
                {"$pull": {"endpoints": {"endpoint_id": endpoint_id}}}
            )
            self.log_service.create_log(webhook_id, endpoint_id, SUCCESS_MESSAGE, RESPONSE_CODE_SUCCESS, "Endpoint deleted successfully")
            return {"message": ENDPOINT_DELETED_MESSAGE}, RESPONSE_CODE_SUCCESS
        except Exception as e:
            self.log_service.create_log(webhook_id, endpoint_id, None, RESPONSE_CODE_ERROR, f"Error deleting endpoint: {e}")
            raise DatabaseError(DATABASE_ERROR_MESSAGE)

    def list_webhooks(self):
        try:
            webhooks = list(self.get_webhook_collection().find())
            for webhook in webhooks:
                webhook["_id"] = str(webhook["_id"])
            self.log_service.create_log(None, None, SUCCESS_MESSAGE, RESPONSE_CODE_SUCCESS, "Webhooks listed successfully")
            return webhooks, RESPONSE_CODE_SUCCESS
        except Exception as e:
            self.log_service.create_log(None, None, None, RESPONSE_CODE_ERROR, f"Error listing webhooks: {e}")
            raise DatabaseError(DATABASE_ERROR_MESSAGE)

    def get_webhook_logs(self, webhook_id):
        try:
            logs = list(self.log_service.get_logs_collection().find({"webhook_id": webhook_id}))
            for log in logs:
                log["_id"] = str(log["_id"])
            return logs, RESPONSE_CODE_SUCCESS
        except Exception as e:
            self.log_service.create_log(webhook_id, None, None, RESPONSE_CODE_ERROR, f"Error getting webhook logs: {e}")
            raise DatabaseError(DATABASE_ERROR_MESSAGE)

    def get_status(self):
        try:
            status = {
                "uptime": UPTIME,
                "total_requests": self.log_service.get_logs_collection().count_documents({}),
                "successful_requests": self.log_service.get_logs_collection().count_documents({"status": SUCCESS_MESSAGE}),
                "failed_requests": self.log_service.get_logs_collection().count_documents({"status": "failure"}),
                "average_latency_ms": AVERAGE_LATENCY_MS
            }
            self.log_service.create_log(None, None, SUCCESS_MESSAGE, RESPONSE_CODE_SUCCESS, "Status retrieved successfully")
            return status, RESPONSE_CODE_SUCCESS
        except Exception as e:
            self.log_service.create_log(None, None, None, RESPONSE_CODE_ERROR, f"Error getting status: {e}")
            raise DatabaseError(DATABASE_ERROR_MESSAGE)

    def receive_webhook(self, webhook_id, data):
        try:
            webhook = self.get_webhook_collection().find_one({"_id": ObjectId(webhook_id)})
            if not webhook:
                raise NotFoundError(WEBHOOK_NOT_FOUND_MESSAGE)

            endpoints = webhook.get("endpoints", [])
            for endpoint in endpoints:
                try:
                    self.forward_to_endpoint(endpoint["url"], data)
                    self.log_service.create_log(webhook_id, endpoint["endpoint_id"], SUCCESS_MESSAGE, RESPONSE_CODE_SUCCESS, "Forwarded successfully")
                except Exception as e:
                    self.log_service.create_log(webhook_id, endpoint["endpoint_id"], None, RESPONSE_CODE_ERROR, f"Error forwarding to endpoint {endpoint['url']}: {e}")
            self.forward_to_endpoint(webhook["webhook_url"], data)
            self.log_service.create_log(webhook_id, None, SUCCESS_MESSAGE, RESPONSE_CODE_SUCCESS, "Webhook received successfully")
            return data, RESPONSE_CODE_SUCCESS
        except NotFoundError as e:
            raise e
        except Exception as e:
            self.log_service.create_log(webhook_id, None, None, RESPONSE_CODE_ERROR, f"Error receiving webhook: {e}")
            raise DatabaseError(DATABASE_ERROR_MESSAGE)

    def forward_to_endpoint(self, endpoint, data):
        try:
            # async with ClientSession() as session:
            #     async with session.post(endpoint, json=data) as response:
            #         if response.status != 200:
            #             raise Exception(f"Endpoint {endpoint} returned status code {response.status}")
                        
            response = requests.post(endpoint, json=data)
            
            if response.status_code != 200:
                
                raise Exception(f"Endpoint {endpoint} returned status code {response.status_code}")
            
        except Exception as e:
            raise Exception(f"Error forwarding to endpoint {endpoint}: {e}")
        
    

