import os
from mongoengine import (
    connect
)
from dotenv import load_dotenv

from room import Room
from sensor import Sensor

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
    area=45.5,
    longitude=100,
    latitude=100
).save()

room2 = Room(
    name="Lobby",
    type="LOBBY",
    crowd_factor=0.3,
    area=120.0,
    longitude=100,
    latitude=100
).save()

# Insert Sensors referencing the Rooms
# "movements" is stored as a list of lists of integers.
sensor1 = Sensor(
    name="Sensor-A",
    movements=[[5, 3], [1, 2]],
    rooms=[room1]
).save()

sensor2 = Sensor(
    name="Sensor-B",
    movements=[[2, 1]],
    rooms=[room1]
).save()

sensor3 = Sensor(
    name="Sensor-C",
    movements=[[10, 7], [4, 3]],
    rooms=[room1, room2]
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
