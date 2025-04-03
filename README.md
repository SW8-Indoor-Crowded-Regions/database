# Indoor Crowded Region Detection Database

This package provides MongoDB models and database access for the Indoor Crowded Region Detection project.

## Installation

if a specific branch is required (like dev)

add @<branchname> to the end

```bash
pip install git+https://github.com/SW8-Indoor-Crowded-Regions/database
```

If you already have an outdated version of the database installed and listed in requirements.txt, run below command to update
```bash
pip install --upgrade --no-cache-dir -r requirements.txt
```

## Usage

First, ensure you have a `.env` file with your MongoDB connection string:

```env
MONGO_URL=your_mongodb_connection_string
```

Then you can use the package like this:

```python
from db.database import Database
from db.models.room import Room

# Initialize database connection
db = Database()

# Create and save a new room
room = Room(
    name="please my god",
    type="LOBBY",
    crowd_factor=0.3,
    area=120.0,
    longitude=100,
    latitude=100
).save()

# Verify data was persisted
all_rooms = Room.objects()
# Print rooms with their details
for room in all_rooms:
    print(f"Room: {room.name} (Type: {room.type}, Area: {room.area}m², Crowd Factor: {room.crowd_factor})")
```

## Models

### Room
- name (string): Name of the room
- type (string enum): MEETING, LOBBY, or OFFICE
- crowdFactor (double): How crowded the room is
- area (double): Total area in square units
- longitude (double): longitude coordinate
- latitude (double): latitude coordinate

### Sensor
- name (string): Sensor identifier
- movements (array of [int, int]): Movement counts in two directions
- roomId (ObjectId): Reference to the room
