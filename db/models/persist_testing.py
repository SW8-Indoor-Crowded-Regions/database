# persist_and_test.py

import os
import datetime
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# Import the validators from the separate files
from room import rooms_validator
from sensor import sensors_validator
from visitor import visitors_validator

# --------------------------------------
# 1) Load environment variables & connect to MongoDB
# --------------------------------------
load_dotenv()
uri = os.getenv("MONGO_URL", "")
client = MongoClient(uri, server_api=ServerApi('1'))

# Select the database (make sure this matches your setup)
db = client["indoor-crowd"]

# Ping the server to confirm the connection
try:
    db.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("Error during ping:", e)

# --------------------------------------
# 2) Create collections with schema validation
# --------------------------------------
try:
    db.create_collection("rooms", validator=rooms_validator)
    print("Created 'rooms' collection with schema validation.")
except Exception as e:
    print("rooms collection might already exist:", e)

try:
    db.create_collection("sensors", validator=sensors_validator)
    print("Created 'sensors' collection with schema validation.")
except Exception as e:
    print("sensors collection might already exist:", e)

try:
    db.create_collection("visitors", validator=visitors_validator)
    print("Created 'visitors' collection with schema validation.")
except Exception as e:
    print("visitors collection might already exist:", e)

# --------------------------------------
# 3) Insert sample documents
# --------------------------------------

# Insert two Rooms
room1 = db.rooms.insert_one({
    "name": "Conference Room",
    "type": "MEETING",
    "crowdFactor": 0.8,
    "area": 45.5
})

room2 = db.rooms.insert_one({
    "name": "Lobby",
    "type": "LOBBY",
    "crowdFactor": 0.3,
    "area": 120.0
})

# Insert Sensors referencing the Rooms
# Note: "movements" is now an array of tuples (each tuple is represented as an array of 2 integers)
sensor1 = db.sensors.insert_one({
    "name": "Sensor-A",
    "movements": [[5, 3], [1, 2]],  # Example: two tuples representing different movement counts
    "roomId": room1.inserted_id
})

sensor2 = db.sensors.insert_one({
    "name": "Sensor-B",
    "movements": [[2, 1]],  # One tuple in an array
    "roomId": room1.inserted_id
})

sensor3 = db.sensors.insert_one({
    "name": "Sensor-C",
    "movements": [[10, 7], [4, 3]],  # Two tuples for room2
    "roomId": room2.inserted_id
})

# Insert Visitors
visitor1 = db.visitors.insert_one({
    "name": "John Doe",
    "visitedRooms": [room1.inserted_id],
    "visitDate": datetime.datetime.now()
})

visitor2 = db.visitors.insert_one({
    "name": "Jane Smith",
    "visitedRooms": [room1.inserted_id, room2.inserted_id],
    "visitDate": datetime.datetime.now()
})

# --------------------------------------
# 4) Create indexes (optional, for performance)
# --------------------------------------
db.rooms.create_index("name")
db.sensors.create_index("name")
db.visitors.create_index("name")

# --------------------------------------
# 5) Query examples
# --------------------------------------
print("\nAll Rooms:")
for r in db.rooms.find():
    print(r)

print("\nAll Sensors:")
for s in db.sensors.find():
    print(s)

print("\nAll Visitors:")
for v in db.visitors.find():
    print(v)

print(f"\nVisitors who visited room1 (id={room1.inserted_id}):")
for v in db.visitors.find({"visitedRooms": room1.inserted_id}):
    print(v)

# Close the client if desired
client.close()
