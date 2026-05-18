import os
from pathlib import Path

try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure
except ImportError:
    MongoClient = None

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
DATABASE_NAME = os.getenv('DB_NAME', 'groundwater_system')


def get_mongo_client():
    if MongoClient is None:
        raise ImportError('pymongo is required for MongoDB support. Install it with pip install pymongo')
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    return client


def get_dataset_collection():
    client = get_mongo_client()
    return client[DATABASE_NAME]['datasets']


def log_alert(alert):
    client = get_mongo_client()
    collection = client[DATABASE_NAME]['alerts']
    collection.insert_one(alert)


def fetch_alerts(limit=10):
    client = get_mongo_client()
    collection = client[DATABASE_NAME]['alerts']
    return list(collection.find().sort('created_at', -1).limit(limit))
