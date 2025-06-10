
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os

class Database:
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self.connect()
    
    def connect(self):
        try:
            # Connect to local MongoDB
            self._client = MongoClient('mongodb://localhost:27017/')
            self._db = self._client['task_manager']
            
            # Test connection
            self._client.admin.command('ping')
            print("Connected to MongoDB successfully!")
            
        except ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise
    
    def get_database(self):
        return self._db
    
    def get_collection(self, collection_name):
        return self._db[collection_name]
    
    def close_connection(self):
        if self._client:
            self._client.close()

# Global database instance
db_instance = Database()