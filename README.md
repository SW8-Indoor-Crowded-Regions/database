# Indoor Crowded Region Detection Database

This package provides MongoDB models and database access for the Indoor Crowded Region Detection project.

## Installation

```bash
pip install indoor-crowded-region-detection-database
```

## Usage

First, ensure you have a `.env` file with your MongoDB connection string:

```env
MONGO_URL=your_mongodb_connection_string
```

Then you can use the package like this:

```python
from models import Database, rooms_validator, sensors_validator, visitors_validator

# Connect to database
db = Database()

# Example: Insert a room
room = db.rooms.insert_one({
    "name": "Conference Room",
    "type": "MEETING",
    "crowdFactor": 0.8,
    "area": 45.5
})

# Example: Query rooms
all_rooms = list(db.rooms.find())

# Example: Insert a sensor for the room
sensor = db.sensors.insert_one({
    "name": "Sensor-A",
    "movements": [[5, 3], [1, 2]],
    "roomId": room.inserted_id
})

# Example: Insert a visitor
visitor = db.visitors.insert_one({
    "name": "John Doe",
    "visitedRooms": [room.inserted_id],
    "visitDate": datetime.datetime.now()
})

# Don't forget to close the connection when done
db.close()
```

## Schema Validation

The package includes MongoDB schema validators for all collections. You can access them directly if needed:

```python
from models import rooms_validator, sensors_validator, visitors_validator

# Example: Print the rooms schema
print(rooms_validator)
```

## Models

### Room
- name (string): Name of the room
- type (string enum): MEETING, LOBBY, or OFFICE
- crowdFactor (double): How crowded the room is
- area (double): Total area in square units

### Sensor
- name (string): Sensor identifier
- movements (array of [int, int]): Movement counts in two directions
- roomId (ObjectId): Reference to the room

### Visitor
- name (string): Visitor name
- visitedRooms (array of ObjectId): Rooms visited
- visitDate (date): Optional visit date
