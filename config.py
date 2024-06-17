import os
from dotenv import load_dotenv
from pymongo import MongoClient 

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
# SECRET_KEY = os.getenv("SECRET_KEY")

mongo = MongoClient(MONGO_URI)
db = mongo['webhook_db']
