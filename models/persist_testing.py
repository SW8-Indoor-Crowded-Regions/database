import os
import datetime
from mongoengine import (
    connect
)
from dotenv import load_dotenv

from room import Room
from sensor import Sensor
from visitor import Visitor

# --------------------------------------
# 1) Load environment variables & connect to MongoDB
# --------------------------------------
load_dotenv()
uri = os.getenv("MONGO_URL", "")
db_name = "indoor-crowd"

# Connect to MongoDB using MongoEngine
connect(db=db_name, host=uri)
print("Connected to MongoDB via MongoEngine!")


# --------------------------------------
# 3) Insert sample documents
# --------------------------------------

# Insert two Rooms
room1 = Room(
    name="Conference Room",
    type="MEETING",
    crowd_factor=0.8,
    area=45.5
).save()

room2 = Room(
    name="Lobby",
    type="LOBBY",
    crowd_factor=0.3,
    area=120.0
).save()

# Insert Sensors referencing the Rooms
# "movements" is stored as a list of lists of integers.
sensor1 = Sensor(
    name="Sensor-A",
    movements=[[5, 3], [1, 2]],
    room=room1
).save()

sensor2 = Sensor(
    name="Sensor-B",
    movements=[[2, 1]],
    room=room1
).save()

sensor3 = Sensor(
    name="Sensor-C",
    movements=[[10, 7], [4, 3]],
    room=room2
).save()

# Insert Visitors
visitor1 = Visitor(
    name="John Doe",
    visited_rooms=[room1],
    visit_date=datetime.datetime.now()
).save()

visitor2 = Visitor(
    name="Jane Smith",
    visited_rooms=[room1, room2],
    visit_date=datetime.datetime.now()
).save()

# --------------------------------------
# 4) Query examples
# --------------------------------------
print("\nAll Rooms:")
for r in Room.objects:
    print(r.to_json())

print("\nAll Sensors:")
for s in Sensor.objects:
    print(s.to_json())

print("\nAll Visitors:")
for v in Visitor.objects:
    print(v.to_json())

print(f"\nVisitors who visited room1 (id={room1.id}):")
for v in Visitor.objects(visited_rooms=room1):
    print(v.to_json())
