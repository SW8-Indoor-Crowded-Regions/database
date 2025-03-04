import os
from dotenv import load_dotenv
from mongoengine import connect

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", None)

if not MONGO_URL:
    raise ValueError("MONGO_URL is not set!")

connect(host=MONGO_URL)
print("Connected to MongoDB")
