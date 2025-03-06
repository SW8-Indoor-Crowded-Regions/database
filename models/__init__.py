from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

class Database:
    def __init__(self):
        load_dotenv()
        uri = os.getenv("MONGO_URL", "")
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client["indoor-crowd"]
        
        # Ensure collections exist with validators
        self._ensure_collections()
        
        # Create properties for easy access to collections
        self.rooms = self.db.rooms
        self.sensors = self.db.sensors
    
    def _ensure_collections(self):
        """Ensure collections exist with proper validation"""
        collections = self.db.list_collection_names()
        
        if "rooms" not in collections:
            self.db.create_collection("rooms", validator=rooms_validator)
        
        if "sensors" not in collections:
            self.db.create_collection("sensors", validator=sensors_validator)
            
    def close(self):
        """Close the database connection"""
        self.client.close()

# Export validators for reference
__all__ = [
    'Database'
]
